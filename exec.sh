#!/bin/bash
pip install --upgrade azure-cli
# Login to Azure
az login -u lasal.Hettiarachchi@studentambassadors.com -p todmaj-tiJsyd-0sybri
# Run UVicorn
uvicorn main:app --host 0.0.0.0 --port 8000
