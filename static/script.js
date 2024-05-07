function toggleBtn() {
  const answerDiv = document.getElementById('answer');
  const changeButton = document.getElementById('changeButton');

  // Change button text and functionality
  if (changeButton.value === 'Show') {
    changeButton.value = 'Next';
    answerDiv.style.backgroundColor = 'rgba(255, 255, 255, 0.45)';
  } else {
    changeButton.value = 'Show';
    answerDiv.style.backgroundColor = 'black';
    submitForm();
  }
}

function submitForm() {
  const answerDiv = document.getElementById('answer');
  const questionDiv = document.getElementById('question');
  const numberDiv = document.getElementById('number');
  const formData = new FormData(document.getElementById('submit-form'));

  fetch('/submit', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    answerDiv.textContent = data.answer;
    questionDiv.textContent = data.question;
    numberDiv.value = data.number;
  })
  .catch(error => {
    console.error('Error sending request:', error);
  });
}


