# MCP Completion Service

A simple Python-based Model Context Protocol (MCP) service that implements the `attempt_completion` tool for signaling task completion in AI workflows.

## Overview

This service provides a standardized way for AI agents to signal when they have completed a task, along with a summary of what was accomplished. It's designed to be lightweight, easy to integrate, and extensible for various completion tracking needs.

## Features

- **MCP Protocol Compliant**: Implements JSON-RPC 2.0 over stdin/stdout
- **Simple Integration**: Easy to add to existing MCP client configurations
- **Extensible**: Built with customization points for specific use cases
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Robust error handling with proper MCP error responses

## Installation

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Setup

1. Clone or download the `completion_service.py` file
2. Make it executable:
   ```bash
   chmod +x completion_service.py
   ```

## Usage

### Running the Service

The service runs as a standalone script that communicates via stdin/stdout:

```bash
# Normal operation with logging
python mcp_attempt_completion.py

# Quiet mode (no logging output)
python mcp_attempt_completion.py --quiet
# or
python mcp_attempt_completion.py -q

# Using environment variable to disable logging
MCP_QUIET=1 python mcp_attempt_completion.py
```

### MCP Client Configuration

#### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "completion-service": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_attempt_completion.py"]
    }
  }
}
```

For quiet mode (no logging), add the `--quiet` flag:
```json
{
  "mcpServers": {
    "completion-service": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_attempt_completion.py", "--quiet"]
    }
  }
}
```

Or use the environment variable:
```json
{
  "mcpServers": {
    "completion-service": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_attempt_completion.py"],
      "env": {
        "MCP_QUIET": "1"
      }
    }
  }
}
```

#### Other MCP Clients

Configure the service using the command:
```bash
python /path/to/mcp_attempt_completion.py
```

### Tool Usage

Once configured, the `attempt_completion` tool will be available in your MCP client:

```python
# Example usage in an AI workflow
attempt_completion(result="Successfully processed 150 files and generated summary report")
```

## Tool Schema

### attempt_completion

**Description**: Signal that a task has been completed with a result summary

**Parameters**:
- `result` (string, required): A summary of what was accomplished

**Example**:
```json
{
  "name": "attempt_completion",
  "arguments": {
    "result": "Data analysis complete. Processed 1,000 records, identified 3 anomalies, and generated visualization dashboard."
  }
}
```

## Customization

The service is designed to be easily extensible. You can modify the `_attempt_completion` method to add custom behavior:

### Example Extensions

#### Save to File
```python
async def _attempt_completion(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    result = arguments.get("result", "")
    
    # Save to completion log
    with open("completions.log", "a") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp}: {result}\n")
    
    # ... rest of method
```

#### Send Webhook
```python
import aiohttp

async def _attempt_completion(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    result = arguments.get("result", "")
    
    # Send webhook notification
    async with aiohttp.ClientSession() as session:
        await session.post("https://hooks.slack.com/your-webhook", 
                          json={"text": f"Task completed: {result}"})
    
    # ... rest of method
```

#### Database Storage
```python
import sqlite3

async def _attempt_completion(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    result = arguments.get("result", "")
    
    # Store in database
    conn = sqlite3.connect("completions.db")
    conn.execute("INSERT INTO completions (timestamp, result) VALUES (?, ?)", 
                 (datetime.now(), result))
    conn.commit()
    conn.close()
    
    # ... rest of method
```

## Configuration

The service can be configured by modifying the class initialization:

```python
class MCPServer:
    def __init__(self, config_file=None):
        # Load configuration from file if provided
        if config_file:
            with open(config_file) as f:
                config = json.load(f)
        # ... configure based on settings
```

## Logging

The service includes comprehensive logging that can be controlled via command line arguments or environment variables.

### Logging Control

**Command Line:**
```bash
# Normal logging (default)
python mcp_attempt_completion.py

# Disable all logging
python mcp_attempt_completion.py --quiet
python mcp_attempt_completion.py -q
```

**Environment Variable:**
```bash
# Disable logging via environment variable
MCP_QUIET=1 python mcp_attempt_completion.py
MCP_QUIET=true python mcp_attempt_completion.py
MCP_QUIET=yes python mcp_attempt_completion.py
```

**Programmatic Control:**
You can also modify the `setup_logging()` function to customize logging behavior:

```python
def setup_logging(quiet: bool = False):
    if quiet:
        logging.basicConfig(level=logging.CRITICAL + 1)  # Disable all
    else:
        logging.basicConfig(level=logging.INFO)  # Normal logging
        # Or use logging.DEBUG for verbose output
        # Or use logging.WARNING for minimal output
```

### What Gets Logged

When logging is enabled, the service logs:
- Service startup/shutdown
- Tool execution attempts
- Error conditions
- Request/response processing

## Troubleshooting

### Common Issues

1. **Service not starting**
   - Check Python version (3.7+ required)
   - Verify file permissions
   - Check for syntax errors with `python -m py_compile completion_service.py`

2. **Tool not appearing in client**
   - Verify MCP client configuration
   - Check absolute paths in configuration
   - Restart MCP client after configuration changes

3. **JSON errors**
   - Ensure proper MCP client setup
   - Check stdin/stdout isn't being interfered with by other processes
   - Enable debug logging to see raw messages

### Debug Mode

Enable verbose logging for troubleshooting:

```python
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

## Development

### Adding New Tools

To add additional tools, extend the `tools` dictionary in `__init__`:

```python
self.tools["new_tool"] = {
    "name": "new_tool",
    "description": "Description of the new tool",
    "inputSchema": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
}
```

Then add a handler method:

```python
async def _new_tool(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    # Implementation here
    pass
```

### Testing

Test the service manually by sending JSON-RPC messages:

```bash
echo '{"jsonrpc": "2.0", "id": "1", "method": "initialize", "params": {}}' | python completion_service.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is released under the MIT License. See LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review MCP protocol documentation
- Open an issue with detailed error messages and configuration details