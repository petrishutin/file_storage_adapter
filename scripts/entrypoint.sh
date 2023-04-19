#!/bin/bash
export LOG_LEVEL

sleep 10

if [ -z "$LOG_LEVEL" ];
then
    LOG_LEVEL='INFO'
fi

if [ -z "$PORT" ];
then
    PORT=8000
fi

uvicorn main:app --host 0.0.0.0 --port "$PORT" --log-level "${LOG_LEVEL,,}"
