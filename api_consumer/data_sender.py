import asyncio
import argparse
import logging
import random
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

import aiohttp
import schedule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("data_sender")

class ServerDataSender:
    def __init__(
        self,
        api_url: str = "http://localhost:8000",
        frequency: float = 1.0,
        num_servers: int = 1,
        username: str = "admin",
        password: str = "admin"
    ):
        """
        Initialize the data sender service.
        
        Args:
            api_url: Base URL of the API
            frequency: Frequency in Hz (1-10)
            num_servers: Number of servers to create
            username: Username for authentication
            password: Password for authentication
        """
        self.api_url = api_url
        self.frequency = min(max(frequency, 1.0), 10.0)  # Clamp between 1 and 10 Hz
        self.delay = 1.0 / self.frequency  # Convert Hz to seconds
        self.num_servers = num_servers
        self.username = username
        self.password = password
        self.auth_token = None
        self.server_ids = []
        self.session = None
        self.running = False
    
    async def initialize(self):
        """Initialize HTTP session, authenticate, and register servers."""
        self.session = aiohttp.ClientSession()
        
        # Authenticate first
        self.auth_token = await self._authenticate()
        if not self.auth_token:
            logger.error("Failed to authenticate. Exiting.")
            return False
            
        # Register servers
        if self.num_servers > 0:
            logger.info(f"Starting registration of {self.num_servers} servers")
            for i in range(self.num_servers):
                server_name = f"Dolly{random.randint(1000, 9999)}"
                server_id = await self._register_server(server_name)
                if server_id:
                    self.server_ids.append(server_id)
                    logger.info(f"Server {server_name} registered with ID: {server_id}")
                
            logger.info(f"Successfully registered {len(self.server_ids)} servers")
            
        return len(self.server_ids) > 0
    
    async def _authenticate(self) -> Optional[str]:
        """Register user or login and return the auth token."""
        # First try to register
        try:
            register_data = {
                "username": self.username,
                "password": self.password,
                "email": f"{self.username}@example.com"
            }
            
            async with self.session.post(
                f"{self.api_url}/auth/register", 
                json=register_data
            ) as response:
                if response.status == 201:
                    logger.info("User registered successfully")
                elif response.status == 409:
                    logger.info("User already exists, proceeding to login")
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to register user. Status: {response.status}, Response: {error_text}")
                    return None
        except Exception as e:
            logger.error(f"Exception during user registration: {e}")
            
        # Now login to get the token
        try:
            form_data = {
                "username": self.username,
                "password": self.password
            }
            
            async with self.session.post(
                f"{self.api_url}/auth/login", 
                data=form_data
            ) as response:
                if response.status == 200:
                    resp_data = await response.json()
                    token = resp_data.get("access_token")
                    logger.info("Authentication successful")
                    return token
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to login. Status: {response.status}, Response: {error_text}")
                    return None
        except Exception as e:
            logger.error(f"Exception during login: {e}")
            return None
    
    async def _register_server(self, server_name: str, max_attempts: int = 5) -> Optional[str]:
        """Register a new server and return its ID, retry with different name if 409."""
        if not self.auth_token:
            logger.error("Auth token required to register server")
            return None
            
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        attempt = 0
        
        while attempt < max_attempts:
            # Generate a new name if this is a retry
            if attempt > 0:
                server_name = f"Dolly{random.randint(1000, 9999)}"
                
            data = {"server_name": server_name}
            
            try:
                async with self.session.post(
                    f"{self.api_url}/servers", 
                    json=data,
                    headers=headers
                ) as response:
                    if response.status == 201:
                        resp_data = await response.json()
                        return resp_data.get("server_ulid")
                    elif response.status == 409:
                        logger.warning(f"Server name '{server_name}' already exists, trying another name")
                        attempt += 1
                        continue
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to register server. Status: {response.status}, Response: {error_text}")
                        return None
            except Exception as e:
                logger.error(f"Exception during server registration: {e}")
                return None
                
        logger.error(f"Failed to register server after {max_attempts} attempts")
        return None
    
    async def _generate_reading(self, server_id: str) -> Dict[str, Any]:
        timestamp = datetime.now().isoformat()
        
        reading = {
            "server_ulid": server_id,
            "timestamp": timestamp,
            "temperature": round(random.uniform(0, 100), 2),
            "voltage": round(random.uniform(0, 220), 2),
            "current": round(random.uniform(0, 10), 2),
            "humidity": round(random.uniform(0, 100), 2)
        }
        return reading
    
    async def _send_reading(self, reading: Dict[str, Any]) -> bool:
        """Send a reading to the API."""
        try:
            async with self.session.post(
                f"{self.api_url}/data", 
                json=reading
            ) as response:
                if response.status == 201:
                    resp_data = await response.json()
                    logger.debug(f"Reading sent successfully: {resp_data}")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to send reading. Status: {response.status}, Response: {error_text}")
                    return False
        except Exception as e:
            logger.error(f"Exception sending reading: {e}")
            return False

    async def start_sending(self):
        """Start sending readings at the specified frequency for all servers."""
        if not self.server_ids:
            logger.error("No servers registered to send readings")
            return
            
        self.running = True
        logger.info(f"Starting to send readings for {len(self.server_ids)} servers at {self.frequency}Hz (every {self.delay:.4f} seconds)")
        
        while self.running:
            start_time = time.time()
            
            for server_id in self.server_ids:
                reading = await self._generate_reading(server_id)
                success = await self._send_reading(reading)
                
                if success:
                    logger.info(f"Sent reading for server {server_id}")
            
            # Calculate sleep time to maintain frequency
            elapsed = time.time() - start_time
            sleep_time = max(0, self.delay - elapsed)
            
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
    
    def stop(self):
        """Stop the sending process."""
        self.running = False
        logger.info("Stopping data sending service")
    
    async def cleanup(self):
        """Close the HTTP session."""
        if self.session:
            await self.session.close()
            logger.info("HTTP session closed")


async def main():
    parser = argparse.ArgumentParser(description="Server data sender service")
    parser.add_argument("--api-url", type=str, default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--frequency", type=float, default=1.0, help="Frequency in Hz (1-10)")
    parser.add_argument("--num-servers", type=int, default=1, help="Number of servers to create")
    parser.add_argument("--username", type=str, default="admin", help="Username for authentication")
    parser.add_argument("--password", type=str, default="admin", help="Password for authentication")
    
    args = parser.parse_args()
    
    # Environment variables override command line arguments
    api_url = os.environ.get("API_URL", args.api_url)
    frequency = float(os.environ.get("FREQUENCY", args.frequency))
    num_servers = int(os.environ.get("NUM_SERVERS", args.num_servers))
    username = os.environ.get("USERNAME", args.username)
    password = os.environ.get("PASSWORD", args.password)
    
    sender = ServerDataSender(
        api_url=api_url,
        frequency=frequency,
        num_servers=num_servers,
        username=username,
        password=password
    )
    
    initialized = await sender.initialize()
    if not initialized:
        logger.error("Failed to initialize the data sender. Exiting.")
        return
    
    try:
        await sender.start_sending()
    except KeyboardInterrupt:
        logger.info("Service interrupted by user")
    except Exception as e:
        logger.error(f"Service error: {e}")
    finally:
        sender.stop()
        await sender.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
