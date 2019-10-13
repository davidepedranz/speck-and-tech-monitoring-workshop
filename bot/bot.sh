#!/bin/sh

# read the backend URL from the environment
backend="${BACKEND:-'http://localhost:5000'}"

while true
do

    # calls to a not-existing endpoint
    for _ in $(seq 20); do
        curl -s -X GET "${backend}/speck" > /dev/null
    done

    # calls to existing endpoints
    for _ in $(seq 10); do

        # create a Todo
        text="I am a robot 🤖"
        id=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"text\": \"${text}\"}" "${backend}/todos/" | jq --raw-output ".id")

        # update the Todo
        text="I am a robot 🤖 and I like 🐖"
        curl -s -X PATCH -H "Content-Type: application/json" -d "{\"text\": \"${text}\"}" "${backend}/todos/${id}" > /dev/null

        # activate and deactivate the Todo
        curl -s -X POST "${backend}/todos/${id}/activate" > /dev/null
        curl -s -X POST "${backend}/todos/${id}/deactivate" > /dev/null

        # get the single Todo and the list
        curl -s -X GET "${backend}/todos/${id}" > /dev/null
        curl -s -X GET "${backend}/todos/" > /dev/null

        # delete the Todo
        curl -s -X DELETE "${backend}/todos/${id}" > /dev/null

        # create and delete a Todo, possibly bugged 🐞
        id=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"text\": \"🤖 likes speck 🐖\"}" "${backend}/todos/" | jq --raw-output ".id")
        curl -s -X DELETE "${backend}/todos/${id}" > /dev/null
    done

    # do not overheat your laptop 💻
    sleep 1
done
