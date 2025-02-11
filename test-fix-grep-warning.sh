#!/bin/bash

test_delay_extraction() {
    local message="$1"
    local expected_hours="$2"
    local expected_minutes="$3"
    local expected_seconds="$4"
    local expected_total_seconds="$5"
    local expected_delay="$6"

    if echo "$message" | grep -q 'capture will start in'; then
        is_delay=true
    else
        is_delay=false
    fi

    delay_hours=$(echo "$message" | grep -Eo "[0-9]+ hour" | grep -Eo "[0-9]*")
    delay_minutes=$(echo "$message" | grep -Eo "[0-9]+ minute" | grep -Eo "[0-9]*")
    delay_seconds=$(echo "$message" | grep -Eo "[0-9]+ second" | grep -Eo "[0-9]*")

    [[ $delay_hours =~ ^[0-9]+$ ]] || delay_hours="0"
    [[ $delay_minutes =~ ^[0-9]+$ ]] || delay_minutes="0"
    [[ $delay_seconds =~ ^[0-9]+$ ]] || delay_seconds="0"

    total_delay_seconds=$((delay_hours * 3600 + delay_minutes * 60 + delay_seconds))

    if $expected_delay; then
        if [[ $delay_hours == $expected_hours && $delay_minutes == $expected_minutes && $delay_seconds == $expected_seconds && $total_delay_seconds == $expected_total_seconds && $is_delay == $expected_delay ]]; then
            echo "Test passed for message: $message"
        else
            echo "Test failed for message: $message"
            echo "Expected hours: $expected_hours, got: $delay_hours"
            echo "Expected minutes: $expected_minutes, got: $delay_minutes"
            echo "Expected seconds: $expected_seconds, got: $delay_seconds"
            echo "Expected total seconds: $expected_total_seconds, got: $total_delay_seconds"
            echo "Expected delay: $expected_delay, got: $is_delay"
        fi
    else
        if [[ $is_delay == $expected_delay ]]; then
            echo "Test passed for message: $message"
        else
            echo "Test failed for message: $message"
            echo "Expected delay: $expected_delay, got: $is_delay"
        fi
    fi
}

# Test cases
test_delay_extraction 'The same snapshot had been made 30 minutes ago. You can make new capture of this URL after 1 hour.' 0 0 0 0 false
test_delay_extraction 'The capture will start in ~1 hour, 1 minute because our service is currently overloaded. You may close your browser window and the page will still be saved.' 1 1 0 3660 true
test_delay_extraction 'The capture will start in ~1 hour, 2 minutes because our service is currently overloaded. You may close your browser window and the page will still be saved.' 1 2 0 3720 true
test_delay_extraction 'The capture will start in ~2 hours, 1 minutes because our service is currently overloaded. You may close your browser window and the page will still be saved.' 2 1 0 7260 true
test_delay_extraction 'The capture will start in ~3 hours, 11 minutes because our service is currently overloaded. You may close your browser window and the page will still be saved.' 3 11 0 11460 true
test_delay_extraction 'The capture will start in ~1 minute, 1 second because our service is currently overloaded. You may close your browser window and the page will still be saved.' 0 1 1 61 true
test_delay_extraction 'The capture will start in ~1 minute, 2 seconds because our service is currently overloaded. You may close your browser window and the page will still be saved.' 0 1 2 62 true
test_delay_extraction 'The capture will start in ~2 minutes, 1 second because our service is currently overloaded. You may close your browser window and the page will still be saved.' 0 2 1 121 true
test_delay_extraction 'The capture will start in ~2 minutes, 2 seconds because our service is currently overloaded. You may close your browser window and the page will still be saved.' 0 2 2 122 true
test_delay_extraction 'The capture will start in ~1 hour because our service is currently overloaded. You may close your browser window and the page will still be saved.' 1 0 0 3600 true
test_delay_extraction 'The capture will start in ~3 hours because our service is currently overloaded. You may close your browser window and the page will still be saved.' 3 0 0 10800 true
test_delay_extraction 'The capture will start in ~1 minute because our service is currently overloaded. You may close your browser window and the page will still be saved.' 0 1 0 60 true
test_delay_extraction 'The capture will start in ~2 minutes because our service is currently overloaded. You may close your browser window and the page will still be saved.' 0 2 0 120 true
test_delay_extraction 'The capture will start in ~1 second because our service is currently overloaded. You may close your browser window and the page will still be saved.' 0 0 1 1 true
test_delay_extraction 'The capture will start in ~50 seconds because our service is currently overloaded. You may close your browser window and the page will still be saved.' 0 0 50 50 true
test_delay_extraction 'The capture will start in ~4 hours, 30 minutes because our service is currently overloaded. You may close your browser window and the page will still be saved.' 4 30 0 16200 true

# Run test by command:
#     bash test-fix-grep-warning.sh
