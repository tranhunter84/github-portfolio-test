#!/bin/bash

# Set the number of test runs as a variable
NUM_TESTS=125
TREE_SIZE=50

# Clear tracking.txt to avoid appending to old results
> ../data/tracking.txt

# Run the program NUM_TESTS times
for ((i=1; i<=NUM_TESTS; i++))
do
    echo "Running game $i..."
    python3 p2_play.py mcts_modified mcts_vanilla
done

# Generate the graph using a Python script
python3 - <<END
import matplotlib.pyplot as plt

# Read results from tracking.txt
with open('../data/tracking.txt', 'r') as file:
    data = file.readlines()

# Convert data to integers
results = [int(line.strip()) for line in data]

# Generate game numbers
game_numbers = list(range(1, len(results) + 1))

# Count cumulative wins for each player
player1_cumulative = []
player2_cumulative = []

player1_wins = 0
player2_wins = 0

for result in results:
    if result == 1:
        player1_wins += 1
    else:
        player2_wins += 1
    player1_cumulative.append(player1_wins)
    player2_cumulative.append(player2_wins)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(game_numbers, player1_cumulative, label="mcts_modified Wins", marker='o')
plt.plot(game_numbers, player2_cumulative, label="mcts_vanilla Wins", marker='x')

# Add graph details
plt.title(f"Cumulative Wins Over {len(results)} Games With Tree Size of $TREE_SIZE")
plt.xlabel("Game Number")
plt.ylabel("Cumulative Wins")
plt.ylim(0, $NUM_TESTS)  # Set y-axis max to NUM_TESTS
plt.legend()
plt.grid(True)

# Save and display the graph
plt.savefig('../data/game_results.png')
plt.show()
END
