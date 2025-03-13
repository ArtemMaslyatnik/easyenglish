//add word in list 
$(document).ready(function () {
  // отслеживаем событие отправки формы
    $('form').submit(function (e) {
      var data_id = $(this).attr('data-wb')
      if (typeof data_id === typeof undefined) 
        {
          console.log(0)
          return 0; 
        }
    e.preventDefault();
    //test del
    console.log(location.href);
    // создаем AJAX-вызов
    $.ajax({
      data: $(this).serialize(), // получаем данные формы
      type: $(this).attr('method'), // GET или POST

      url: $("#url-wordbook").attr("data-url"),
      // если успешно, то
      success: function (response) {
        if (response.wordbook_list === true) {
          $('#insertWordbook_'+response.id).hide()
          $('#removeWordbook_'+response.id).show()
        } else if (response.wordbook_list === false) {
          if (response.wordbook === 'wordbook') {
            $('#wordbook_item_'+response.id).hide()
          }          
          else
            $('#removeWordbook_'+response.id).hide()
            $('#insertWordbook_'+response.id).show()
          
        }
      },
      // если ошибка, то
      error: function (response) {
        // предупредим об ошибке
        alert(response.responseJSON.errors)
        console.log(response.responseJSON.errors)
      }
    })
    return false
  })
})


//add comment 
$(document).ready(function () {
  // отслеживаем событие отправки формы
  $('#create-comment').submit(function () {
    // создаем AJAX-вызов
    $.ajax({
      data: $(this).serialize(), // получаем данные формы
      type: $(this).attr('method'), // GET или POST

      url: $("#url-comment").attr("data-url"),
      // если успешно, то
      success: function (response) {
        let StrComment = getStrComment(response.comment)
        $('#comments').append(StrComment);
        $('#textarea-comment').val('');
        

      },
      // если ошибка, то
      error: function (response) {
        // предупредим об ошибке
        alert(response.responseJSON.errors)
        console.log(response.responseJSON.errors)
      }
    })
    return false
  })
})


//add subcomment
// отслеживаем событие отправки формы
$(document).on("click", "#btn-create-sub-comment", function (e) {

    //let form = $("#create-sub-comment").serialize();
    // создаем AJAX-вызов
    $.ajax({
      url: $("#url-sub-comment").attr("data-url"),
      //событие клик по кнопке а данные в форме
      type: $(this).parent().attr('method'), // GET или POST
      data: $(this).parent().serialize(),  // получаем данные формы
  //    dataType: 'html', // если успешно, то

      success: function (response) {
        let StrComment = getSubStrComment(response.comment)
        $('#comment-parent-'+ response.comment.parent +'').append(StrComment);
        $('#textarea-sub-comment').val('');
       },
      // если ошибка, то
      error: function (response) {
        // предупредим об ошибке
        //alert(response.responseJSON.errors)
        //console.log(response.responseJSON.errors)

      }
    })
    return false 
});       


//add form subcomment
$(document).ready(function () {
  // отслеживаем событие отправки формы
  $('.sub-comment-link').on('click', function (event) {
      event.preventDefault();
      const csrf = getCookie('csrftoken');
      let idSubComment = $(this).attr('id');
      idSubComment = idSubComment.replace('sub-comment-', '')
      $('#create-sub-comment').remove();
      let formComment = getFormComment(csrf, idSubComment);
      $('#comment-parent-'+idSubComment).append(formComment);
    })
})

//translate sentence
$(document).on("click", "#sentence", function (e) {

    let idx = $(this).attr("data-index");
    // создаем AJAX-вызов
     $.ajax({
      url: "/book/translate/",
      //событие клик по кнопке а данные в форме
      type: "GET", // GET или POST
      data: {"idSentence": idx },

      success: function (response) {
        $("#translate").css("display", "block");
        $("#page-content").children().css("backgroundColor", "#FFFFFF");
        $('[data-index=' + idx +']').css("backgroundColor", "#F7F70F");
        $('#translate').text(response.translate);
        

      },
      // если ошибка, то
      error: function (response) {
        // предупредим об ошибке
        //alert(response.responseJSON.errors)
        //console.log(response.responseJSON.errors)

      }
    })
    return false 
}); 


//hiden translate sentence
$(document).on("click", "#translate", function (e) {
  $("#translate").css("display", "none");
}); 


//translate word
$(document).on("dblclick", "#word", function (e) {

  let word = $(this).text();

  // создаем AJAX-вызов
   $.ajax({
    url: "/book/translateWord/",
    //событие клик по кнопке а данные в форме
    type: "GET", // GET или POST
    data: {"Word": word},

    success: function (response) {
      text ="";
      $("#translate-word").css("display", "block");
      for (Item in response.word) {
      count = 0;         
      if (Item === "related") {
        if (response.word[Item].length > 0) { 
          text = text + "<div>" + getTranslatePartSpeech(Item);
          for (kay in response.word[Item]){
            count++;
            text = text + response.word[Item][kay].fields.relate_english_word + (count != response.word[Item].length ? ", ": "");
          }
          text = text + "</div>" 
        }
      } else {
        if (response.word[Item].length > 0) { 
          text = text + "<div>" + getTranslatePartSpeech(Item);
          for (kay in response.word[Item]){
            count++;
            text = text + response.word[Item][kay].fields.russian + (count != response.word[Item].length ? ", ": "");
          }
          text = "<div>"+ text + "</div> </div>"      
        }
      }
    }
    $('#translate-word').empty().append(text);


    },
    // если ошибка, то
    error: function (response) {
       // предупредим об ошибке
      //alert(response.responseJSON.errors)
      //console.log(response.responseJSON.errors)

    }
  })
  return false 
}); 


//hiden translate word
$(document).on("click", "#translate-word", function (e) {

      $("#translate-word").css("display", "none");
  
}); 


//servis function
function getStrComment(comment){

  return '<div class="row">'
  + '<div class="col">'
  + '  <div class="d-flex flex-start">'
  + '    <img class="rounded-circle shadow-1-strong me-3"'
  + '      src="' + comment.image + '" alt="avatar" width="65"'
  + '      height="65" />'
  + '    <div class="flex-grow-1 flex-shrink-1">'
  + '      <div>'
  + '        <div class="d-flex justify-content-between align-items-center">'
  + '          <p class="mb-1">'
  +             comment.user +'<span class="small"> ' + comment.created +'</span>'
  + '          </p>'
  + '          <a href="#!"><i class="fas fa-reply fa-xs"></i><span class="small">ответ</span></a>'
  + '        </div>'
  + '        <p class="small mb-0">'
  +            comment.text 
  + '        </p>'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + ' </div>'
  + ' </div>'

}


function getFormComment(csrf, idCommen){

  return  '<form id="create-sub-comment" method="post" >'
  + '<input type="hidden" id="url-sub-comment" data-url="/comment/create/'+ idCommen + '/"/>'
  + '<input type="hidden" name="parent-comment" value="'+ idCommen + '"/>'
  + '<input type="hidden" name="csrfmiddlewaretoken" value="'+ csrf +'">'
  + '<textarea id="textarea-sub-comment" name="text" class="form-control" aria-label="With textarea"></textarea>'
  + '<button id="btn-create-sub-comment" type="submit" class="btn btn-outline-primary mt-1 ">Отправить</button>'
  + '</form>'

}

function getSubStrComment(comment){
 
  return '<div class="row">'
  + '<div class="col">'
  + '  <div class="d-flex flex-start">'
  + '    <img class="rounded-circle shadow-1-strong me-3"'
  + '      src="' + comment.image + '" alt="avatar" width="65"'
  + '      height="65" />'
  + '    <div class="flex-grow-1 flex-shrink-1">'
  + '      <div>'
  + '        <div class="d-flex justify-content-between align-items-center">'
  + '          <p class="mb-1">'
  +             comment.user +'<span class="small"> ' + comment.created +'</span>'
  + '          </p>'
  + '        </div>'
  + '        <p class="small mb-0">'
  +            comment.text 
  + '        </p>'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + ' </div>'
  + ' </div>'
}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function getTranslatePartSpeech (word) {
  switch(word) {
    case 'adjective':   
      return "Прилагательное(ы): "
    case 'adverb':   
      return "Наречие(я): "
      
    case 'conjunction':   
      return "Союз(ы): "
      
    case 'fpos':   
      return "Функциональные части речи:"
    case 'noun':   
      return "Существительное(ые): "
    case 'preposition':   
      return "Предлог(и): "
     case 'pronoun':   
      return "Местоимение(я): "
    case 'verb':   
      return "Глагол(ы): "
    case 'related':   
      return "Родственные словоформы: "
    default:
      return "Др.: "
  }

}
