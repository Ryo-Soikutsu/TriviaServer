# TriviaServer
Simple CTF socat server to allow participants to connect to the server, and answer questions in exchange for a flag. 
## How to use
Questions can be configured in `config.json`, using the following format

    {
    	"question": "your question here",
    	"answer": "your answer here",
    	"hint": "optional hint to guide players"
    }

If no hint is specified, the server will default to a redacted form of the answer
- E.g. if the answer is "192.168.123.45", the hint will display "***.***.***.**" instead. 

Flags can be configured in Dockerfile, in the FLAG environmental variable
`ENV FLAG=YOUR_FLAG_HERE`


