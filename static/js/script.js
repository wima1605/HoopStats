document.addEventListener('DOMContentLoaded', function() {
    let currentComparisonType = ''; // This will be updated when data is fetched
    bindEventListeners();
    fetchInitialData();
    updateScoreDisplays();
    const homeIconLink = document.querySelector('.home-icon-link');

// Reset the current score to 0 when clicking on the home icon
homeIconLink.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default link behavior
    let currentScoreKey = `currentScore_${currentComparisonType}`;
    localStorage.setItem(currentScoreKey, '0'); // Reset the current score to 0
    window.location.href = this.href; // Redirect to the homepage
});

    function bindEventListeners() {
        document.addEventListener('click', function(event) {
            if (event.target.matches('.higherButton') || event.target.matches('.lowerButton')) {
                event.preventDefault();
                makeChoice(event.target.dataset.choice);
            }
        });
    }
    function GameOver(high_score) {
        fetch('/game_over', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({high_score: high_score})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();  // Expecting JSON now
        })
        .then(data => {
            window.location.href = data.redirect_url;  // Use the redirect URL provided by the server
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    }
    
    
    
    function fetchInitialData() {
        let currentScoreKey = `currentScore_${currentComparisonType}`;
        localStorage.setItem(currentScoreKey, '0'); 
        fetch('/get-players')
            .then(response => response.json())
            .then(data => {
                currentComparisonType = data.comparisonType; // Store the comparison type
                PlayerDisplay(data, currentComparisonType);
                updateScoreDisplays(); // Update scores based on the current type
            })
            .catch(error => console.error('Error fetching player info:', error));
    }

    function fetchUpdatedData() {
        fetch('/correct_guess')
            .then(response => response.json())
            .then(data => {
                currentComparisonType = data.comparisonType;
                PlayerDisplay(data, currentComparisonType);
                updateScoreDisplays();
            })
            .catch(error => console.error('Error fetching player info:', error));
    }

    function PlayerDisplay(data, comparisonType) {
        const player1Info = document.getElementById('player1-info');
        const player2Info = document.getElementById('player2-info');
        let comparisonText;
        let player1Stat;
        let player2Stat;
    
        switch (comparisonType) {
            case 'career_scoring_average':
                comparisonText = 'Career PPG Average';
                player1Stat = data.player1.ppg;
                player2Stat = data.player2.ppg;
                break;
            case 'single_season_ppg':
                comparisonText = 'Highest Single Season PPG';
                player1Stat = data.player1.ppg;
                player2Stat = data.player2.ppg;
                break;
            case 'career_fg_percent':
                comparisonText = 'Career FG Percentage';
                player1Stat = `${data.player1.fgp}%`; // Assuming FG% is stored as a plain number
                player2Stat = `${data.player2.fgp}%`;
                break;
            case 'career_blocks':
                comparisonText = 'Career Blocks';
                player1Stat = `${data.player1.bc}`; // Assuming FG% is stored as a plain number
                player2Stat = `${data.player2.bc}`;
                break;
            default:
                comparisonText = 'PPG Average';
                player1Stat = data.player1.ppg;
                player2Stat = data.player2.ppg;
        }
    
        player1Info.innerHTML = data.player1 ? `
            <strong>${data.player1.full_name}</strong><br>
            ${comparisonText}: ${player1Stat}<br>
            <img src="${data.player1.image}" alt="${data.player1.full_name} Image">
        ` : 'Player data not available';
    
        player2Info.innerHTML = data.player2 ? `
            <strong>Does ${data.player2.full_name} have a</strong><br>
            <div class="button-container">
                <button class="higherButton" data-choice="higher">Higher</button>
                <button class="lowerButton" data-choice="lower">Lower</button>
            </div>
            ${comparisonText}<br>
            <img src="${data.player2.image}" alt="${data.player2.full_name} Image">
        ` : 'Player data not available';
    }
    
   
    function makeChoice(choice) {
        fetch(`/guess/${choice}`, { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                let currentScoreKey = `currentScore_${currentComparisonType}`;
                let highestScoreKey = `highestScore_${currentComparisonType}`;
                if (data.correct_guess) {
                    let currentScore = parseInt(localStorage.getItem(currentScoreKey)) || 0;
                    currentScore++;
                    localStorage.setItem(currentScoreKey, currentScore);
                    fetchUpdatedData();
                } else {
                    let currentScore = parseInt(localStorage.getItem(currentScoreKey)) || 0;
                    let highestScore = parseInt(localStorage.getItem(highestScoreKey)) || 0;
                    if (currentScore > highestScore) {
                        localStorage.setItem(highestScoreKey, currentScore);
                    }
                    localStorage.removeItem(currentScoreKey);
                    console.log('Redirecting with High Score:', localStorage.getItem(highestScoreKey));
                    GameOver(localStorage.getItem(highestScoreKey));
                }
                updateScoreDisplays();

            })
            .catch(error => console.error('Error:', error));
    }

    function updateScoreDisplays() {
        let currentScoreKey = `currentScore_${currentComparisonType}`;
        let highestScoreKey = `highestScore_${currentComparisonType}`;
        const currentScoreDisplay = document.getElementById('current-score');
        const highestScoreDisplay = document.getElementById('highest-score');
        let highestScore = parseInt(localStorage.getItem(highestScoreKey)) || 0;
        let currentScore = parseInt(localStorage.getItem(currentScoreKey)) || 0;
        currentScoreDisplay.textContent = currentScore;
        highestScoreDisplay.textContent = highestScore;
    }
});
