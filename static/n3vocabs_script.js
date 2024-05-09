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
    const kanjiDiv = document.getElementById('kanji');
    const definitionDiv = document.getElementById('definition');
    const hiraganaDiv = document.getElementById('hiragana');
    const numberDiv = document.getElementById('number');
    const formData = new FormData(document.getElementById('submit-form'));
  
    radio = document.getElementById('radio-in-order');
    if(radio.checked){
      formData.append('radio', 'inorder');
    }else{
      formData.append('radio', 'random');
    }
  
    fetch('/nextn3vocab', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      kanjiDiv.textContent = data.kanji;
      definitionDiv.textContent = data.definition;
      hiraganaDiv.textContent = data.hiragana;
      numberDiv.value = data.number;
    })
    .catch(error => {
      console.error('Error sending request:', error);
    });
  }
  
  function toggleRadio(){
    random_inputsDiv = document.getElementById('random-inputs');
    radio = document.getElementById('radio-in-order');
    if(radio.checked){
      random_inputsDiv.style.display = 'none';
    }else{
      random_inputsDiv.style.display = 'block';
    }
  }
  
  function goBtn(){
    const answerDiv = document.getElementById('answer');
    answerDiv.style.backgroundColor = 'black';
    const changeButton = document.getElementById('changeButton');
    changeButton.value = 'Show';
    numberDiv = document.getElementById('number');
    number = parseInt(numberDiv.value);
    number--;
    numberDiv.value = number;
    submitForm();
  }
  