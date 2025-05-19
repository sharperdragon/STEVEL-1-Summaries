

// Toggle quiz mode to hide/reveal autoantibody answers
let quizMode = false;

function toggleQuizMode() {
  quizMode = !quizMode;
  const cells = document.querySelectorAll('.quiz-answer');
  cells.forEach(cell => {
    if (quizMode) {
      cell.classList.add('hidden-answer');
      cell.addEventListener('click', revealAnswer);
    } else {
      cell.classList.remove('hidden-answer');
      cell.removeEventListener('click', revealAnswer);
    }
  });
}

// Reveal the answer on cell click
function revealAnswer(event) {
  event.currentTarget.classList.remove('hidden-answer');
}