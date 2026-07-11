# HTTP 418: "I'm a teapot"

This is a joke status code that means the server refuses to brew coffee because it is, permanently, a teapot.

## Origin
It comes from the **Hyper Text Coffee Pot Control Protocol (HTCPCP)**, defined in **RFC 2324**, published on April 1, 1998 (an April Fools' joke RFC by the IETF).

## Purpose
The original RFC was a parody that imagined a protocol for controlling coffee pots. The 418 status code was meant to be returned if you asked a teapot to brew coffee—since a teapot cannot perform that action.

## Real-World Usage
Despite being a joke, the code gained genuine popularity:
- **Google** implemented it in some of their APIs as an easter egg
- **Node.js**, various web frameworks, and libraries have built-in support for it
- It's occasionally used by developers as a fun/humorous response in APIs or demos
- Some services use it intentionally to indicate "this isn't the right request for this endpoint" in a lighthearted way

## Official Status
Interestingly, **RFC 7168** (published in 2014) formally documented HTCPCP-TEA, expanding on the joke and further cementing 418 in a semi-official capacity within IETF documentation—though it remains outside the standard HTTP status codes used in serious API design (like 200, 404, 500, etc.).

So while you probably won't encounter it in production systems, it's a fun piece of internet culture that occasionally pops up in developer humor or Easter eggs.