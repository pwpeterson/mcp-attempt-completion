#!/usr/bin/env python3
"""
MCP Service implementing attempt_completion tool
"""

import asyncio
import json
import sys
import os
import argparse
from typing import Any, Dict, List, Optional, Union
import logging

# Configure logging based on environment variable or command line argument
def setup_logging(quiet: bool = False):
    """Setup logging configuration"""
    # Check LOGGING_ON environment variable first
    logging_on = os.getenv('LOGGING_ON', 'true').lower()
    
    if quiet or logging_on in ('false', '0', 'no', 'off'):
        # Disable all logging
        logging.basicConfig(level=logging.CRITICAL + 1)
    else:
        # Normal logging (default when LOGGING_ON is 'true' or not set)
        logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

# Will be initialized in main()
logger = None


class MCPServer:
    """Simple MCP Server implementation with attempt_completion tool"""
    
    def __init__(self):
        self.tools = {
            "attempt_completion": {
                "name": "attempt_completion",
                "description": "Signal that a task has been completed with a result summary",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "result": {
                            "type": "string",
                            "description": "A summary of what was accomplished"
                        }
                    },
                    "required": ["result"]
                }
            }
        }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "initialize":
                return self._handle_initialize(request_id)
            elif method == "tools/list":
                return self._handle_tools_list(request_id)
            elif method == "tools/call":
                return await self._handle_tools_call(request_id, params)
            else:
                return self._error_response(request_id, f"Unknown method: {method}")
                
        except Exception as e:
            if logger and logger.isEnabledFor(logging.ERROR):
                logger.error(f"Error handling request: {e}")
            return self._error_response(request.get("id"), str(e))
    
    def _handle_initialize(self, request_id: Union[str, int, None]) -> Dict[str, Any]:
        """Handle initialization request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "completion-service",
                    "version": "1.0.0"
                }
            }
        }
    
    def _handle_tools_list(self, request_id: Union[str, int, None]) -> Dict[str, Any]:
        """Handle tools list request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": list(self.tools.values())
            }
        }
    
    async def _handle_tools_call(self, request_id: Union[str, int, None], params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "attempt_completion":
            return await self._attempt_completion(request_id, arguments)
        else:
            return self._error_response(request_id, f"Unknown tool: {tool_name}")
    
    async def _attempt_completion(self, request_id: Union[str, int, None], arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of attempt_completion tool"""
        result = arguments.get("result", "")
        
        # Log the completion attempt
        if logger and logger.isEnabledFor(logging.INFO):
            logger.info(f"Task completion attempted with result: {result}")
        
        # You can add custom logic here, such as:
        # - Saving results to a file
        # - Sending notifications
        # - Updating a database
        # - Triggering webhooks
        
        # For this example, we'll just return a success response
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": f"Task completed successfully. Result: {result}"
                    }
                ]
            }
        }
    
    def _error_response(self, request_id: Union[str, int, None], message: str) -> Dict[str, Any]:
        """Create an error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -1,
                "message": message
            }
        }


async def main():
    """Main server loop"""
    global logger
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='MCP Completion Service')
    parser.add_argument('--quiet', '-q', action='store_true', 
                       help='Disable logging output')
    args = parser.parse_args()
    
    # Initialize logging
    logger = setup_logging(quiet=args.quiet)
    
    server = MCPServer()
    if not args.quiet and os.getenv('LOGGING_ON', 'true').lower() not in ('false', '0', 'no', 'off'):
        logger.info("MCP Completion Service started")
    
    try:
        # Read from stdin and write to stdout (MCP transport)
        while True:
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            
            if not line:
                break
                
            try:
                request = json.loads(line.strip())
                response = await server.handle_request(request)
                
                # Write response to stdout
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError as e:
                if logger and logger.isEnabledFor(logging.ERROR):
                    logger.error(f"Invalid JSON received: {e}")
                error_response = server._error_response(None, "Invalid JSON")
                print(json.dumps(error_response), flush=True)
                
    except KeyboardInterrupt:
        if logger and logger.isEnabledFor(logging.INFO):
            logger.info("Server shutting down...")
    except Exception as e:
        if logger and logger.isEnabledFor(logging.ERROR):
            logger.error(f"Server error: {e}")


if __name__ == "__main__":
    asyncio.run(main())