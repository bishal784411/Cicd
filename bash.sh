#!/bin/bash

# Load .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "⏳ Countdown before AI analysis (showing current time each second):"

# Uncomment below to enable countdown
# for ((i=1; i<=30; i++)); do
#     current_time=$(date +"%H:%M:%S")
#     printf "\r   ⏱️  %02d/30 seconds | Time: %s" "$i" "$current_time"
#     sleep 1
# done

echo -e "\n✅ Starting AI analysis now!"

# Use the GEMINI_API_KEY from .env file
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: ${GEMINI_API_KEY}" \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Tell me something about Softwarica college and what are the courses available there."
          }
        ]
      }
    ]
  }'
#!/bin/bash

# Load .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "⏳ Countdown before AI analysis (showing current time each second):"

# Uncomment below to enable countdown
# for ((i=1; i<=30; i++)); do
#     current_time=$(date +"%H:%M:%S")
#     printf "\r   ⏱️  %02d/30 seconds | Time: %s" "$i" "$current_time"
#     sleep 1
# done

echo -e "\n✅ Starting AI analysis now!"

# Use the GEMINI_API_KEY from .env file
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: ${GEMINI_API_KEY}" \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Tell me something about Softwarica college and what are the courses available there."
          }
        ]
      }
    ]
  }'
#!/bin/bash

# Load .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "⏳ Countdown before AI analysis (showing current time each second):"

# Uncomment below to enable countdown
# for ((i=1; i<=30; i++)); do
#     current_time=$(date +"%H:%M:%S")
#     printf "\r   ⏱️  %02d/30 seconds | Time: %s" "$i" "$current_time"
#     sleep 1
# done

echo -e "\n✅ Starting AI analysis now!"

# Use the GEMINI_API_KEY from .env file
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: ${GEMINI_API_KEY}" \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Tell me something about Softwarica college and what are the courses available there."
          }
        ]
      }
    ]
  }'
#!/bin/bash

# Load .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "⏳ Countdown before AI analysis (showing current time each second):"

# Uncomment below to enable countdown
# for ((i=1; i<=30; i++)); do
#     current_time=$(date +"%H:%M:%S")
#     printf "\r   ⏱️  %02d/30 seconds | Time: %s" "$i" "$current_time"
#     sleep 1
# done

echo -e "\n✅ Starting AI analysis now!"

# Use the GEMINI_API_KEY from .env file
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: ${GEMINI_API_KEY}" \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Tell me something about Softwarica college and what are the courses available there."
          }
        ]
      }
    ]
  }'
#!/bin/bash

# Load .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "⏳ Countdown before AI analysis (showing current time each second):"

# Uncomment below to enable countdown
# for ((i=1; i<=30; i++)); do
#     current_time=$(date +"%H:%M:%S")
#     printf "\r   ⏱️  %02d/30 seconds | Time: %s" "$i" "$current_time"
#     sleep 1
# done

echo -e "\n✅ Starting AI analysis now!"

# Use the GEMINI_API_KEY from .env file
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: ${GEMINI_API_KEY}" \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Tell me something about Softwarica college and what are the courses available there."
          }
        ]
      }
    ]
  }'
#!/bin/bash

# Load .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "⏳ Countdown before AI analysis (showing current time each second):"

# Uncomment below to enable countdown
# for ((i=1; i<=30; i++)); do
#     current_time=$(date +"%H:%M:%S")
#     printf "\r   ⏱️  %02d/30 seconds | Time: %s" "$i" "$current_time"
#     sleep 1
# done

echo -e "\n✅ Starting AI analysis now!"

# Use the GEMINI_API_KEY from .env file
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: ${GEMINI_API_KEY}" \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Tell me something about Softwarica college and what are the courses available there."
          }
        ]
      }
    ]
  }'
#!/bin/bash

# Load .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "⏳ Countdown before AI analysis (showing current time each second):"

# Uncomment below to enable countdown
# for ((i=1; i<=30; i++)); do
#     current_time=$(date +"%H:%M:%S")
#     printf "\r   ⏱️  %02d/30 seconds | Time: %s" "$i" "$current_time"
#     sleep 1
# done

echo -e "\n✅ Starting AI analysis now!"

# Use the GEMINI_API_KEY from .env file
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: ${GEMINI_API_KEY}" \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Tell me something about Softwarica college and what are the courses available there."
          }
        ]
      }
    ]
  }'
