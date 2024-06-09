// game variables
let errors = 0;
let numSelected = null;
let solution = null;
let numberCount = Array(9).fill(0); // Array to track count of each number placed on the board
let startTime = null; // Timer start time
let timerInterval = null;
let currentPuzzleId = null; // Store the current puzzle ID

function get_sudoku_from_url() {
    fetch('/get_random_puzzle')
    .then(res => res.json())
    .then(out => {
        currentPuzzleId = out.puzzle_id; // Set the current puzzle ID
        setGame(out);
    })
    .catch(err => { throw err });
}

function setGame(puzzle) {
    // Clear existing board and digits
    document.getElementById("board").innerHTML = '';
    document.getElementById("digits").innerHTML = '';
    
    // Reset game variables
    errors = 0;
    numSelected = null;
    solution = null;
    numberCount.fill(0); // Reset the count array
    document.getElementById("errors").innerText = errors;

    // Reset and start timer
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    startTime = Date.now();
    timerInterval = setInterval(updateTimer, 100);

    let board_string = puzzle['unsolved_board'];
    let solved_string = puzzle['solved_board'];

    // convert string to list, each element with 9 length
    let board = [];
    for (let i = 0; i < board_string.length; i += 9) {
        board.push(board_string.slice(i, i + 9));
    }
    let solved = [];
    for (let i = 0; i < solved_string.length; i += 9) {
        solved.push(solved_string.slice(i, i + 9));
    }
    console.log(board);
    console.log(solved);
    
    solution = solved;
    for (let i = 1; i <= 9; i++) {
        let number = document.createElement("div");
        number.id = i;
        number.innerText = i;
        number.addEventListener("click", selectNumber);
        number.classList.add("number");
        document.getElementById("digits").appendChild(number);
    }

    for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
            let tile = document.createElement("div");
            tile.id = r.toString() + "-" + c.toString();
            // color starting tiles if not 'empty'
            if (board[r][c] != "-") {
                tile.innerHTML = board[r][c];
                tile.classList.add("tile-start");
                numberCount[board[r][c] - 1]++; // Increment count for the initial numbers
            }
            // grid borders, similar to tiktaktoe
            if (r == 2 || r == 5) {
                tile.classList.add("horizontal-line");
            }
            if (c == 2 || c == 5) {
                tile.classList.add("vertical-line");
            }
            // when a tile is clicked
            tile.addEventListener("click", selectTile);
            tile.classList.add("tile");
            document.getElementById("board").append(tile);
        }
    }

    updateDigitsState(); // Update the state of digits based on initial counts
}

function updateTimer() {
    let elapsed = Date.now() - startTime;
    let seconds = Math.floor(elapsed / 1000);
    let milliseconds = elapsed % 1000;
    document.getElementById("timer").innerText = `${seconds}.${milliseconds.toString().padStart(3, '0')}`;
}

function selectNumber() {
    clearHighlights();
    for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
            let tile = document.getElementById(r + "-" + c);
            // Check if the tile has the same innerText as the clicked tile
            if (tile.innerText === this.innerText && this.innerText !== "") {
                // Change the backgroundColor of all the samenum tiles
                if (tile.classList.contains("num-highlight")) {
                    tile.classList.remove("num-highlight");
                } else {
                tile.classList.add("num-highlight");
                }
            } else {
                if (tile.classList.contains("num-highlight")) {
                    tile.classList.remove("num-highlight");
                }
            }
        }
    }
    // select which number should be placeable and highlight it
    if (numSelected != null) {
        numSelected.classList.remove("number-selected");
    }
    if (numSelected === this) {
        numSelected = null;
    } else {
        numSelected = this;
        numSelected.classList.add("number-selected");
    }
}

// resets highlights on board
function clearHighlights() {
    let highlightedTiles = document.querySelectorAll(".tile-highlight");
    // goes through each tile and removes the 'tile-highlight' class
    highlightedTiles.forEach(function(tile) {
        tile.classList.remove("tile-highlight");
    });
}

function clearToggles() {
    let toggledTiles = document.querySelectorAll(".toggle");
    // goes through each tile and removes the 'toggle' class
    toggledTiles.forEach(function(tile) {
        tile.classList.remove("toggle");
    });
}

function selectTile() {
    // get coordinates of tile
    let coordinates = this.id.split("-");
    let r = parseInt(coordinates[0]);
    let c = parseInt(coordinates[1]);
    clearHighlights();
    
    // spaghetti logic for assigning and removing highlights
    if (this.classList.contains("toggle")) {
        this.classList.remove("toggle");
    } else {
        clearToggles();
        this.classList.add("toggle");
        // Highlight tiles on same row (r)
        for (let i=0; i<9; i++) {
            let tileInRow = document.getElementById(r + "-" + i);
            if (tileInRow !== this) {
                // Replace tile-start (gray) to highligt
                tileInRow.classList.add("tile-highlight");
            }
        }

        // Highlight tiles on same column (c)
        for (let i=0; i<9; i++) {
            let tileInColumn = document.getElementById(i + "-" + c);
            if (tileInColumn !== this) {
                // Replace tile-start (gray) to highligt
                tileInColumn.classList.add("tile-highlight");
            }     
        }
    }
    
    // checks for correct placement if variables not null
    if (!this.innerText && numSelected) {
        if (solution[r][c] == numSelected.id) {
            // Correct 
            this.innerText = numSelected.id;
            // only in standardmode (so far need to disable when 'hardcoremode' active)
            this.classList.add("num-highlight");
            numberCount[numSelected.id - 1]++; // Increment the count for the placed number
            updateDigitsState(); // Update the state of digits
            checkCompletion(); // Check if the puzzle is completed
        } else {
            // Incorrect
            errors += 1;
            document.getElementById("errors").innerText = errors;
        }
    }
}

// Update the state of digits based on their counts
function updateDigitsState() {
    for (let i = 1; i <= 9; i++) {
        let numberElement = document.getElementById(i);
        if (numberCount[i - 1] >= 9) {
            numberElement.classList.add("number-disabled");
            numberElement.removeEventListener("click", selectNumber);
        } else {
            numberElement.classList.remove("number-disabled");
            numberElement.addEventListener("click", selectNumber);
        }
    }
}

function checkCompletion() {
    if (numberCount.every(count => count === 9)) {
        clearInterval(timerInterval);
        let elapsed = Date.now() - startTime;
        let seconds = Math.floor(elapsed / 1000);
        let milliseconds = elapsed % 1000;
        alert(`Puzzle completed in ${seconds}.${milliseconds.toString().padStart(3, '0')} seconds with ${errors} mistakes!`);
        saveFastestTime(elapsed, errors);
    }
}

function saveFastestTime(elapsed, mistakes) {
    fetch('/save_fastest_time', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            puzzle_id: currentPuzzleId,
            elapsed: elapsed / 1000, // convert to seconds
            mistakes: mistakes
        })
    })
    .then(response => {
        if (response.status === 401) {
            alert('You are not logged in. Your score was not saved.');
        }
    })
}
