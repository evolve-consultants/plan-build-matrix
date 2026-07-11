# HTTP Status Code 418

**418 I'm a Teapot** is a humorous status code that indicates the server refuses to brew coffee because it is a teapot.

## Details

- **Type**: Client error (4xx)
- **Origin**: Defined in RFC 2324 (April 1, 1998) as an April Fools' joke
- **Actual Use**: Almost never used in production

## Context

This was proposed as a joke for coffee pots that receive requests to brew coffee. The accompanying response body traditionally includes a short poem.

## In Practice

- Most web servers don't implement this code
- Some websites use it humorously (Google has been known to return it in certain contexts)
- It's more of a novelty than a functional HTTP status code

If you encounter it in real life, it's likely either:
1. A server with a sense of humor
2. A misconfiguration
3. Someone testing with the code as a joke

For actual applications, you'd use standard codes like 400 (Bad Request) or 503 (Service Unavailable) instead.