# Hackathon

Project: CLI app for code chef.

## Features

- Submit from terminal (using a hack)
- View problems
- Recommend problems.
- View friends ("look" into their profiles)
- add sets (api provides)

## Architecture
### Client
- Click based CLI
- commands
  - [x] login
    - start OAUTH flow
    - save received tokens
  - [ ] submissions
    - add INPUTFILE --problem-code[-pc] --contest-code[-cc]
    - showall
    - status [uid]
  - [ ] compete
    - show --contest-code[-ci] --filter=[ongoing,past,upcoming]
    - problems --problem-code[-pc] --problem-no[-pn]
