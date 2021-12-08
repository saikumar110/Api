
// Includes custom validations

$(function () {
  'use strict';

  var bootstrapForm = $('.needs-validation'),
    jqForm = $('#jquery-val-form'),
    picker = $('#dob'),
    dtPicker = $('#dob-bootstrap-val'),
    select = $('.select2'),
    infoForm=$("#info_form");

  // select2
  select.each(function () {
    var $this = $(this);
    $this.wrap('<div class="position-relative"></div>');
    $this
      .select2({
        placeholder: 'Select value',
        dropdownParent: $this.parent()
      })
      .change(function () {
        $(this).valid();
      });
  });

  // Picker
  if (picker.length) {
    picker.flatpickr({
      allowInput: true,
      monthSelectorType: 'static',
      onReady: function (selectedDates, dateStr, instance) {
        if (instance.isMobile) {
          $(instance.mobileInput).attr('step', null);
        }
      }
    });
  }

  if (dtPicker.length) {
    dtPicker.flatpickr({
      allowInput: true,
      monthSelectorType: 'static',
      onReady: function (selectedDates, dateStr, instance) {
        if (instance.isMobile) {
          $(instance.mobileInput).attr('step', null);
        }
      }
    });
  }

  // Bootstrap Validation
  // --------------------------------------------------------------------
  if (bootstrapForm.length) {
    Array.prototype.filter.call(bootstrapForm, function (form) {
      form.addEventListener('submit', function (event) {
        if (form.checkValidity() === false) {
          form.classList.add('invalid');
        }
        form.classList.add('was-validated');
        event.preventDefault();
      });
    });
  }

  // jQuery Validation
  // --------------------------------------------------------------------
  //  function for url validation
  function isUrlValid(userInput) {
    var res = userInput.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
    if (res == null)
      return false;
    else
      return true;
  }
  // fnction for phone number validation
  function phoneUS(userInput) {
    var res = userInput.match(/^(\+?1-?)?(\([2-9]\d{2}\)|[2-9]\d{2})-?[2-9]\d{2}-?\d{4}$/);
    if (res == null)
      return false;
    else
      return true;
  }

  $.validator.addMethod("check_url", function (value, element) {
    return isUrlValid(value);
  }, 'Provide the valid url ');


  // Function for Number validation
  $.validator.addMethod("check_phone", function (value, element) {
    return phoneUS(value);
  }, 'Provide the valid phone number ');

  if (infoForm.length){
    infoForm.validate({
      rules: {
        'phone':{
          check_phone: true
        }
      }
    })
  }

  if (jqForm.length) {
    jqForm.validate({
      rules: {
        'basic-default-name': {
          required: true
        },
        'basic-default-email': {
          required: true,
          email: true
        },
        'basic-default-password': {
          required: true
        },
        'confirm-password': {
          required: true,
          equalTo: '#basic-default-password'
        },
        'select-country': {
          required: true
        },
        dob: {
          required: true
        },
        customFile: {
          required: true
        },
        validationRadiojq: {
          required: true
        },
        validationBiojq: {
          required: true
        },
        'facebook': {
          check_url: true
        },
        'twitter': {
          check_url: true
        },
        'google': {
          check_url: true
        },
        'linkedin': {
          check_url: true
        },
        "phone-settings":{
          phoneUs: true
        },
        validationCheck: {
          required: true
        }
      }
    });
  }
});
