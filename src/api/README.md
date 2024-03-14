# Generation / Prompting 

### Idea

**Generation** \
We use Grazie API to generate a prompt. \
The API is passed to handler, which is responsible for validating the response and processing API errors. \

**Prompting** \
Prompter class is responsible for converting a report to a prompt. \
The class uses formatters methods, which are functions activated on each frame or on the whole report. \
Resolvers are used to resolve the config and, consequently, understand which formatter to use. \



### Structure

```
├── generation
│   ├── error_handlers.py - functions to handle errors from Grazie API
│   ├── grazie_api.py
│   ├── handler.py - Handler class
│   └── response_validators.py - functions to validate the response from Grazie API
├── prompter.py - Prompter class
```