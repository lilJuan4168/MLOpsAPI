#!/bin/bash

export PGPASSWORD=1234 && psql -U root -h localhost -d streaming -f ./schema.sql -w  