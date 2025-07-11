#!/bin/bash

echo "⏳ Countdown before AI analysis (showing current time each second):"

# for ((i=1; i<=30; i++)); do
#     current_time=$(date +"%H:%M:%S")
#     printf "\r   ⏱️  %02d/30 seconds | Time: %s" "$i" "$current_time"
#     sleep 1
# done

echo -e "\n✅ Starting AI analysis now!"


curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: AIzaSyC0Z7_WdjYjTJbpaeuVworWH8bMWcIvhTQ' \
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




  