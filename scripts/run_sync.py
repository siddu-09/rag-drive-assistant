"""
Manual sync trigger script.
Usage: python scripts/run_sync.py <folder_id>
"""

import sys
import asyncio
from app.services.sync_service import SyncService


async def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_sync.py <google_drive_folder_id>")
        sys.exit(1)

    folder_id = sys.argv[1]
    service = SyncService()
    result = await service.sync(folder_id)
    print(f"Sync complete: {result}")


if __name__ == "__main__":
    asyncio.run(main())
