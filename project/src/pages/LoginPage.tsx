// import React, { useState } from 'react';
// import { Shield, Mail, Lock, Eye, EyeOff, AlertCircle } from 'lucide-react';
// import { useAuth } from '../hooks/useAuth';
// import { useNavigate } from 'react-router-dom';


// export const LoginPage: React.FC = () => {
//     const navigate = useNavigate();
//     const [email, setEmail] = useState('');
//     const [password, setPassword] = useState('');
//     const [showPassword, setShowPassword] = useState(false);
//     const [error, setError] = useState('');
//     const [isLoading, setIsLoading] = useState(false);
//     const { login } = useAuth();

//       const handleSubmit = async (e: React.FormEvent) => {
//         e.preventDefault();
//         setError('');
//         setIsLoading(true);

//         // Simulate API call delay
//         await new Promise(resolve => setTimeout(resolve, 1000));

//         // Hardcoded credentials
//         const validEmail = 'developer@devsecops.com';
//         const validPassword = 'Developer@1234';

//         if (email === validEmail && password === validPassword) {
//           login({
//             email: email,
//             name: 'DevSecOps Developer',
//             role: 'Administrator'
//           });
//           navigate('/dashboard');

//         } else {
//           setError('Invalid email or password. Please try again.');
//         }

//         setIsLoading(false);
//       };




//     return (
//         <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
//             <div className="w-full max-w-md">
//                 {/* Header */}
//                 <div className="text-center mb-8">
//                     <div className="flex items-center justify-center mb-4">
//                         <div className="p-3 bg-cyan-600 rounded-xl">
//                             <Shield className="h-8 w-8 text-white" />
//                         </div>
//                     </div>
//                     <h1 className="text-3xl font-bold text-white mb-2">DevOps Control Center</h1>
//                     <p className="text-gray-400">Sign in to access your CI/CD dashboard</p>
//                 </div>

//                 {/* Login Form */}
//                 <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 border border-slate-700/50">
//                     <form onSubmit={handleSubmit} className="space-y-6">
//                         {/* Email Field */}
//                         <div>
//                             <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
//                                 Email Address
//                             </label>
//                             <div className="relative">
//                                 <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
//                                     <Mail className="h-5 w-5 text-gray-400" />
//                                 </div>
//                                 <input
//                                     id="email"
//                                     type="email"
//                                     value={email}
//                                     onChange={(e) => setEmail(e.target.value)}
//                                     className="w-full pl-10 pr-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-colors"
//                                     placeholder="Enter your email"
//                                     required
//                                 />
//                             </div>
//                         </div>

//                         {/* Password Field */}
//                         <div>
//                             <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
//                                 Password
//                             </label>
//                             <div className="relative">
//                                 <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
//                                     <Lock className="h-5 w-5 text-gray-400" />
//                                 </div>
//                                 <input
//                                     id="password"
//                                     type={showPassword ? 'text' : 'password'}
//                                     value={password}
//                                     onChange={(e) => setPassword(e.target.value)}
//                                     className="w-full pl-10 pr-12 py-3 bg-slate-700/50 border border-slate-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-colors"
//                                     placeholder="Enter your password"
//                                     required
//                                 />
//                                 <button
//                                     type="button"
//                                     onClick={() => setShowPassword(!showPassword)}
//                                     className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white transition-colors"
//                                 >
//                                     {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
//                                 </button>
//                             </div>
//                         </div>

//                         {/* Error Message */}
//                         {error && (
//                             <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-3 flex items-center space-x-2">
//                                 <AlertCircle className="h-5 w-5 text-red-400 flex-shrink-0" />
//                                 <span className="text-red-300 text-sm">{error}</span>
//                             </div>
//                         )}

//                         {/* Submit Button */}
//                         <button
//                             type="submit"
//                             disabled={isLoading}
//                             className="w-full py-3 px-4 bg-cyan-600 hover:bg-cyan-700 disabled:bg-cyan-800 disabled:opacity-50 text-white font-medium rounded-lg transition-colors flex items-center justify-center space-x-2"
//                         >
//                             {isLoading ? (
//                                 <>
//                                     <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
//                                     <span>Signing in...</span>
//                                 </>
//                             ) : (
//                                 <span>Sign In</span>
//                             )}
//                         </button>
//                     </form>


//                 </div>

//                 {/* Footer */}
//                 <div className="text-center mt-8">
//                     <p className="text-sm text-gray-500">
//                         DevSecOps Control Center
//                     </p>
//                 </div>
//             </div>
//         </div>
//     );
// };

import React, { useState } from 'react';
import { Shield, Mail, Lock, Eye, EyeOff, AlertCircle } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

export const LoginPage: React.FC = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const { login } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            await login({ email, password });
            navigate('/dashboard');
        } catch (error: any) {
            setError(error.message || 'Login failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                {/* Header */}
                <div className="text-center mb-8">
                    <div className="flex items-center justify-center mb-4">
                        <div className="p-3 bg-cyan-600 rounded-xl">
                            <Shield className="h-8 w-8 text-white" />
                        </div>
                    </div>
                    <h1 className="text-3xl font-bold text-white mb-2">DevOps Control Center</h1>
                    <p className="text-gray-400">Sign in to access your CI/CD dashboard</p>
                </div>

                {/* Login Form */}
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 border border-slate-700/50">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Email Field */}
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                                Email Address
                            </label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Mail className="h-5 w-5 text-gray-400" />
                                </div>
                                <input
                                    id="email"
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full pl-10 pr-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-colors"
                                    placeholder="test@example.com"
                                    required
                                />
                            </div>
                        </div>

                        {/* Password Field */}
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                                Password
                            </label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Lock className="h-5 w-5 text-gray-400" />
                                </div>
                                <input
                                    id="password"
                                    type={showPassword ? 'text' : 'password'}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full pl-10 pr-12 py-3 bg-slate-700/50 border border-slate-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-colors"
                                    placeholder="secret"
                                    required
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white transition-colors"
                                >
                                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                                </button>
                            </div>
                        </div>

                        {/* Test Credentials Info */}
                        <div className="bg-blue-500/20 border border-blue-500/50 rounded-lg p-3">
                            <p className="text-blue-300 text-sm">
                                <strong>Test Credentials:</strong><br />
                                Email: test@example.com<br />
                                Password: secret
                            </p>
                        </div>

                        {/* Error Message */}
                        {error && (
                            <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-3 flex items-center space-x-2">
                                <AlertCircle className="h-5 w-5 text-red-400 flex-shrink-0" />
                                <span className="text-red-300 text-sm">{error}</span>
                            </div>
                        )}

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full py-3 px-4 bg-cyan-600 hover:bg-cyan-700 disabled:bg-cyan-800 disabled:opacity-50 text-white font-medium rounded-lg transition-colors flex items-center justify-center space-x-2"
                        >
                            {isLoading ? (
                                <>
                                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                    <span>Signing in...</span>
                                </>
                            ) : (
                                <span>Sign In</span>
                            )}
                        </button>
                    </form>
                </div>

                {/* Footer */}
                <div className="text-center mt-8">
                    <p className="text-sm text-gray-500">
                        DevSecOps Control Center
                    </p>
                </div>
            </div>
        </div>
    );
};