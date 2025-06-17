## Pygame Integration

The application includes interactive game-based challenges using Pygame, which are embedded directly in the browser. These challenges test players' ability to analyze and manipulate memory values to reveal hidden flags.

### Pygame Challenge Features

- **In-Browser Gameplay**: Interactive games run directly in the browser using HTML5 Canvas
- **Memory Manipulation**: Players must discover and manipulate memory values to progress
- **Hidden Flags**: Flags are revealed in parts as players solve different aspects of the game
- **Keyboard Shortcuts**: Special key combinations reveal hidden information (e.g., Ctrl+M to view memory values)
- **Progressive Difficulty**: Players must collect specific values in certain patterns to reveal the complete flag

### Pygame Challenge Example

```javascript
// Check secret values to reveal flag parts
function checkSecretValues() {
    // Check for specific patterns in collected values
    if (collectedValues.includes(42) && !flagRevealed[0]) {
        flagRevealed[0] = true;
        console.log("You found the first part of the flag!");
        updateFlagDisplay();
    }
    
    if (collectedValues.includes(13) && collectedValues.includes(37) && !flagRevealed[1]) {
        flagRevealed[1] = true;
        console.log("You found the second part of the flag!");
        updateFlagDisplay();
    }
    
    // Check if all flag parts have been revealed
    if (flagRevealed.every(part => part)) {
        const flag = flagParts.join('');
        console.log(`FLAG: ${flag}`);
        gameWon(flag);
    }
}
```

### Creating Pygame Challenges

To create a new Pygame challenge:

1. Add a new entry to the `fixtures/initial_data.json` file with `has_pygame` set to `true`
2. Create a JavaScript implementation of the game in the challenge template
3. Define the memory values and patterns required to reveal the flag
4. Implement keyboard shortcuts for revealing hidden information

Pygame challenges add a new dimension to the CTF, requiring players to think about memory manipulation and game mechanics rather than just traditional web vulnerabilities.
