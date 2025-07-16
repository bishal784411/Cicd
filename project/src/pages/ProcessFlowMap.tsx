import React, { useEffect, useState } from 'react';
import {
  Monitor,
  Wrench,
  Hammer,
  GitCommit,
  AlertTriangle,
  CheckCircle,
  Clock,
  Zap,
  Container,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getProcessFlowData } from '../api/push';
import { Breadcrumbs } from '../components/Breadcrumbs';


interface Stage {
  status: 'pending' | 'analyzed' | 'detected' | 'completed' | 'deployed';
  timestamp?: string;
  details: string;
}


interface ErrorFlow {
  id: string;
  errorId: string;
  solutionId: string;
  fixId: string;
  deployId: string;
  title: string;
  description: string;
  icon: React.ComponentType<any>;
  stages: {
    monitor: Stage;
    solution: Stage;
    fix: Stage;
    deploy: Stage;
  };
}



export const ProcessFlowMap: React.FC = () => {
  const navigate = useNavigate();
  const [errorFlows, setErrorFlows] = useState<ErrorFlow[]>([]);

  // Dummy data for individual error flows

  useEffect(() => {
    const fetchData = async () => {
      try {
        const rawData = await getProcessFlowData();

        const parsedFlows: ErrorFlow[] = rawData.map((item: any) => ({
          id: item.id,
          errorId: item.monitor?.error_id,
          solutionId: item.Solution?.solution_id,
          fixId: item.Fix?.fix_id,
          deployId: item.Deploy?.Dep_id,
          title: item.error_type || "Unknown Error",
          description: item.monitor?.error || "No description",
          icon: Container, // You can change based on `error_type` if needed
          stages: {
            monitor: {
              status: 'detected',
              timestamp: item.monitor?.time,
              details: item.monitor?.error || ""
            },
            solution: {
              status: item.Solution?.status || 'pending',
              timestamp: item.Solution?.time,
              details: item.Solution?.analysis || 'No solution yet.'
            },
            fix: {
              status: item.Fix?.status || 'pending',
              timestamp: item.Fix?.time,
              details: item.Fix?.analysis || 'Not fixed yet.'
            },
            deploy: {
              status: item.Deploy?.status || 'pending',
              timestamp: item.Deploy?.time,
              details: item.Deploy?.analysis || 'Not deployed yet.'
            }
          }
        }));

        setErrorFlows(parsedFlows);
      } catch (error) {
        console.error("Failed to fetch process flow data:", error);
      }
    };

    fetchData();
  }, []);

  const getStageStatus = (status: string) => {
    switch (status) {
      case 'detected':
        return { color: 'border-red-500/50 bg-red-500/10 text-red-400', icon: AlertTriangle };
      case 'analyzed':
        return { color: 'border-blue-500/50 bg-blue-500/10 text-blue-400', icon: Zap };
      case 'deployed':
        // return { color: 'border-yellow-500/50 bg-yellow-500/10 text-yellow-400', icon: Clock };
        return { color: 'border-violet-500/50 bg-violet-500/10 text-violet-400', icon: Zap };
      case 'completed':
        return { color: 'border-green-500/50 bg-green-500/10 text-green-400', icon: CheckCircle };
      case 'failed':
        return { color: 'border-red-500/50 bg-red-500/10 text-red-400', icon: AlertTriangle };
      default:
        return { color: 'border-gray-500/50 bg-gray-500/10 text-gray-400', icon: Clock };
    }
  };


  const handleIdClick = (
    e: React.MouseEvent,
    errorFlow: ErrorFlow,
    stageName: string,
    cardId: string
  ) => {
    e.stopPropagation(); // Prevent card click event

    const routeMap: Record<string, string> = {
      monitor: '/monitor',
      solution: '/solution',
      fix: '/fix',
      deploy: '/process flow'
    };

    const route = routeMap[stageName] || '/';

    navigate(route, {
      state: {
        selectedError: errorFlow.id,
        stage: stageName,
        cardId,
        title: errorFlow.title,
        description: errorFlow.description,
        stages: errorFlow.stages
      }
    });

  };
  const StageCard = ({
    title,
    icon: Icon,
    stage,
    errorFlow,
    stageName,
    cardId }: {
      title: string;
      icon: React.ComponentType<any>;
      stage: any;
      errorFlow: ErrorFlow;
      stageName: string;
      cardId: string;
      isLast?: boolean;
    }) => {
    const { color, icon: StatusIcon } = getStageStatus(stage.status);

    return (
      <div className="relative flex-1">
        <div
          className={`relative z-10 p-4 rounded-xl border-2 ${color} bg-slate-800/90 backdrop-blur-sm hover:shadow-xl hover:shadow-cyan-500/20`}
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <Icon className="h-6 w-6" />
              <button
                onClick={(e) => handleIdClick(e, errorFlow, stageName, cardId)}
                className="text-xs font-mono text-cyan-400 hover:text-cyan-300 hover:underline transition-colors duration-200 bg-transparent border-none cursor-pointer p-0"
              >
                {cardId}
              </button>
            </div>
            <StatusIcon className="h-4 w-4" />
          </div>
          <h4 className="font-semibold text-white mb-1 text-sm">{title}</h4>
          <div className="text-xs opacity-80 mb-2 capitalize">{stage.status}</div>
          {stageName === 'deploy' ? (
            <a
              href={`https://github.com/bishal784411/Cicd/commit/${stage.details}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs opacity-70 text-cyan-400 hover:underline break-all"
            >
              {stage.details}
            </a>
          ) : (
            <p className="text-xs opacity-70">{stage.details}</p>
          )}
          {stage.timestamp && (
            <div className="text-xs text-gray-500 mt-2">
              {new Date(`${new Date().toDateString()} ${stage.timestamp}`).toLocaleTimeString()}
            </div>
          )}
        </div>
      </div>
    );
  };

  const currentPage = "Process flow";
  return (
    <div className="space-y-8">
      <Breadcrumbs currentPage={currentPage} parentPage="dashboard" />
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 sm:p-6 border border-slate-700/50">


        <h3 className="text-lg font-semibold text-white mb-2">CI/CD Individual Error Flow</h3>
        <p className="text-sm mb-6 bg-yellow-500/20 border border-yellow-500/50 rounded-xl p-4 text-yellow-200">

          <span className='text-violet-400 font-semibold italic'>Note:</span> 
          <br />
          To see the detailed view of a stage, click the corresponding <span className="text-cyan-400  font-semibold italic">ID</span>.
          <br />
          For the <span className="text-violet-400 font-semibold italic">Deploy</span> stage, click the Git commit <span className="italic text-cyan-400 font-semibold">hash</span> to view the deployment on GitHub.
        </p>

        <div className="space-y-8">
          {errorFlows.map((errorFlow: ErrorFlow) => {
            const ErrorIcon = errorFlow.icon;

            return (
              <div key={errorFlow.id} className="bg-slate-900/30 rounded-lg p-4 border border-slate-700/30">
                {/* Error Header */}
                <div className="flex items-center space-x-3 mb-4">
                  <ErrorIcon className="h-6 w-6 text-cyan-400" />
                  <div>
                    <h4 className="font-semibold text-white">{errorFlow.title}</h4>
                    <p className="text-sm text-gray-400">{errorFlow.description}</p>
                  </div>
                </div>

                {/* Desktop Layout */}
                <div className="hidden lg:block">
                  <div className="relative">
                    {/* Connection Line - Behind cards with z-0 */}
                    <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-slate-600 via-slate-500 to-slate-600 transform -translate-y-1/2 z-0"></div>

                    {/* Stage Cards - Above line with z-10 */}
                    <div className="relative z-10">
                      <div className="grid grid-cols-4 gap-6">
                        <StageCard
                          title="Monitor"
                          icon={Monitor}
                          stage={errorFlow.stages.monitor}
                          errorFlow={errorFlow}
                          stageName="monitor"
                          cardId={errorFlow.errorId}
                        />
                        <StageCard
                          title="Solution"
                          icon={Wrench}
                          stage={errorFlow.stages.solution}
                          errorFlow={errorFlow}
                          stageName="solution"
                          cardId={errorFlow.solutionId}
                        />
                        <StageCard
                          title="Fix"
                          icon={Hammer}
                          stage={errorFlow.stages.fix}
                          errorFlow={errorFlow}
                          stageName="fix"
                          cardId={errorFlow.fixId}
                        />
                        <StageCard
                          title="Deploy"
                          icon={GitCommit}
                          stage={errorFlow.stages.deploy}
                          errorFlow={errorFlow}
                          stageName="deploy"
                          cardId={errorFlow.deployId}
                          isLast={true}
                        />
                      </div>
                      {/* Dots aligned exactly under each StageCard */}
                      <div className="absolute top-1/2 left-0 w-full h-0 pointer-events-none z-5">
                        <div className="grid grid-cols-4 gap-6 relative">
                          {[0, 1, 2, 3].map((_, i) => (
                            <div
                              key={i}
                              className="flex justify-center relative"
                            >
                              <div className="w-3 h-3 bg-slate-400 rounded-full transform -translate-y-1/2 z-5" />
                            </div>
                          ))}
                        </div>
                      </div>

                    </div>
                  </div>
                </div>

                {/* Tablet Layout (3+1) */}
                <div className="hidden md:block lg:hidden">
                  <div className="space-y-4">
                    {/* First row: 3 cards */}
                    <div className="relative">
                      {/* Horizontal line for first 3 cards */}
                      <div className="absolute top-1/2 left-0 right-1/3 h-0.5 bg-gradient-to-r from-slate-600 to-slate-500 transform -translate-y-1/2 z-0"></div>
                      <div className="relative z-10 grid grid-cols-3 gap-4">
                        <StageCard
                          title="Monitor"
                          icon={Monitor}
                          stage={errorFlow.stages.monitor}
                          errorFlow={errorFlow}
                          stageName="monitor"
                          cardId={errorFlow.errorId}
                        />
                        <StageCard
                          title="Solution"
                          icon={Wrench}
                          stage={errorFlow.stages.solution}
                          errorFlow={errorFlow}
                          stageName="solution"
                          cardId={errorFlow.solutionId}
                        />
                        <StageCard
                          title="Fix"
                          icon={Hammer}
                          stage={errorFlow.stages.fix}
                          errorFlow={errorFlow}
                          stageName="fix"
                          cardId={errorFlow.fixId}
                        />

                      </div>
                    </div>

                    {/* Vertical connector */}
                    <div className="flex justify-end pr-16">
                      <div className="w-0.5 h-8 bg-slate-500 z-0"></div>
                    </div>

                    {/* Second row: 1 card */}
                    <div className="flex justify-end">
                      <div className="w-1/3">
                        <StageCard
                          title="Deploy"
                          icon={GitCommit}
                          stage={errorFlow.stages.deploy}
                          errorFlow={errorFlow}
                          stageName="deploy"
                          cardId={errorFlow.deployId}
                          isLast={true}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Mobile Layout */}
                <div className="md:hidden">
                  <div className="space-y-4 relative">
                    {/* Vertical line behind all cards */}
                    <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-slate-500 transform -translate-x-1/2 z-0"></div>

                    {[
                      { title: 'Monitor', icon: Monitor, stage: errorFlow.stages.monitor, stageName: 'monitor', cardId: errorFlow.errorId },
                      { title: 'Solution', icon: Wrench, stage: errorFlow.stages.solution, stageName: 'solution', cardId: errorFlow.solutionId },
                      { title: 'Fix', icon: Hammer, stage: errorFlow.stages.fix, stageName: 'fix', cardId: errorFlow.fixId },
                      { title: 'Deploy', icon: GitCommit, stage: errorFlow.stages.deploy, stageName: 'deploy', cardId: errorFlow.deployId }
                    ].map((stageData, index, array) => (
                      <div key={index} className="relative z-10">
                        <StageCard
                          title={stageData.title}
                          icon={stageData.icon}
                          stage={stageData.stage}
                          errorFlow={errorFlow}
                          stageName={stageData.stageName}
                          cardId={stageData.cardId}
                          isLast={index === array.length - 1}
                        />

                        {/* Connection dots on the line */}
                        <div className="absolute left-1/2 top-1/2 w-3 h-3 bg-slate-400 rounded-full transform -translate-x-1/2 -translate-y-1/2 z-5"></div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );

};