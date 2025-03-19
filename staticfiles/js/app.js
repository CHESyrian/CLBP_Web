$(document).ready(function() {
  // Add Repair Details Element "class repreq-g3"  //
  var repairDetailsElemnt = $('.repreq-g3-container').html();
  $('.add-g3-button').click(function() {
    $('.repreq-g3-container').append(repairDetailsElemnt);
  });
  $('#accordion').accordion();
  $('#accordion').accordion('enable');
  $('#accordion-2').accordion();
  $('#accordion-2').accordion('enable');
  /*   */
  /* Add Repair Request AJAX Request */
  $('.add-repreq-form').submit(function(e) {
    e.preventDefault();
    let $form      = $(this);
    let data       = $form.serialize();
    let url        = $form.attr('action');
    makeElementDisabled($('.save-repreq-btn'), 'جار الحفظ..');
    $.ajax({
      type    :'POST',
      url     : url,
      data    : data,
      success : function(response) {
        TemporaryToast('Success', 'AutoWidth', 'Top', response.Message , 5);
        $('.repreq-g1 :input').val('');
        $('.repreq-g1 label').text('');
        $('.repreq-g2 :input').val('');
        $('.repreq-g3 :input').val('');
        makeElementEnabled($('.save-repreq-btn'), 'حفظ');
        $('.repreq-g3-container').html(repairDetailsElemnt);
      },
      error   : function(response){
        TemporaryToast('Error', 'AutoWidth', 'Top', response.Message , 5);
        makeElementEnabled($('.save-repreq-btn'), 'حفظ');
      },
    });
  })
  /* Add New Field to g3 container to add New Repairs */
  var repreq_g3_edit = $('.repreq-g3-edit').html();
  $('.add-g3edit-button').on('click', function() {
    $('.repreq-g3-edit-container').append('<div class="repreq-g3-edit">' + repreq_g3_edit + '</div>');
  });
  /* Edit & Delete Forms */
  $('.get-editform').on('click', function() {
    let reqID = $("input[name='RepReq_No']").val() + "_" + $("input[name='RepReq_Year']").val()
    let editType = $('.edit-type').val();
    let url = window.origin + "/mech_dep/" + editType + "/" + reqID + "/";
    $.getJSON(url, function(response) {
      if (!response.Status) {
        let msg_toast = response.Message;
        TemporaryToast('Error', 'AutoWidth', 'Top', msg_toast, 5);
      }
      else {
        let Data = response.Data
        if (editType == 'getRepairRequestData') {
          editRepairRequestData(Data);
        } else if (editType == 'getRepairsDetails') {
          editRepairsDetails(Data);
        } else if (editType == 'getRepairsDetailsD') {
          deleteRepairsDetails(Data);
        }
      };
    });
  });
  /* --- Edit Repair Request Ajax Request --- */
  $('.edit-repreq-form').submit(function(e) {
    e.preventDefault();
    let $form      = $(this);
    let data       = $form.serialize();
    let url        = $form.attr('action');
    makeElementDisabled($('.edit-repreq-btn'), 'جار الحفظ..');
    $.ajax({
      type    :'POST',
      url     : url,
      data    : data,
      success : function(response) {
        TemporaryToast('Success', 'AutoWidth', 'Top', response.Message , 5);
        makeElementEnabled($('.edit-repreq-btn'), 'حفظ التغييرات');
        $('.edit-repreq-btn').hide();
        $('.edit-repreqdata-form, .edit-repairsdetails-form, .delete-repairsdetails-form').hide();
        $('.editdetails-form').css('display', 'flex');
      },
      error   : function(response){
        TemporaryToast('Error', 'AutoWidth', 'Top', response.Message , 5);
        makeElementEnabled($('.edit-repreq-btn'), 'حفظ التغييرات');
      },
    });
  })
  $()
  /*  Give Aggrement Function */
  $('input[name=Give_Aggrement]').on('click', function() {
    let clsName    = this.className.split(' ')[1];
    let repreq_id  = clsName.split('-')[3];
    let url        = window.origin + "/fin_dep/giveAggrement/" + repreq_id + "/";
    let csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    let data = {
      'csrfmiddlewaretoken' : csrf_token,
      'RepReq_ID'           : repreq_id,
      'Approval'            : $('input[name=Approval]').val()
    };
    $.ajax({
      type    :'POST',
      url     : url,
      data    : data,
      success : function(response) {
        TemporaryToast('Success', 'AutoWidth', 'Top', response.Message , 5);
        $('.' + clsName).prop('disabled', true);
        $('.' + clsName).addClass('Disabled');
        $('.' + clsName).val('موافق');
      },
      error   : function(response){
        TemporaryToast('Error', 'AutoWidth', 'Top', response.Message , 5);
      },
    });
  });
  /* Add Receipt Page */
  var receipt_g2_element = $('.receipt-g2').html();
  var receipt_g3_element = $('.receipt-g3').html();
  $('.add-receipt-button').on('click', function() {
    $('.receipt-g2-container').append('<div class="receipt-g2 my-5">' + receipt_g2_element + '</div>');
  });
  $('.get-receipt-details').on('click', function() {
    let repreq_no = $('input[name=RepReq_No]').val();
    let req_year  = $('input[name=Year]').val();
    let repreq_id = repreq_no +'_' + req_year;
    let url       = window.origin + "/mech_dep/getRepairsDetails/" + repreq_id + "/";
    $.getJSON(url, function(response) {
      if (!response.Status) {
        let msg_toast = response.Message;
        TemporaryToast('Error', 'AutoWidth', 'Top', msg_toast, 5);
      } else {
        Add_Receipt(response.Data);
      }
    });
  });
  /* --- Save Receipt Function --- */
  $('.add-receipt-form').submit(function(e) {
    e.preventDefault();
    let $form      = $(this);
    let data       = $form.serialize();
    let url        = $form.attr('action');
    makeElementDisabled($('.save-repreq-btn'), 'جار الحفظ..');
    $.ajax({
      type    :'POST',
      url     : url,
      data    : data,
      success : function(response) {
        TemporaryToast('Success', 'AutoWidth', 'Top', response.Message , 5);

        makeElementEnabled($('.save-repreq-btn'), 'حفظ');
        $('.repreq-g3-container').html(repairDetailsElemnt);
      },
      error   : function(response){
        TemporaryToast('Error', 'AutoWidth', 'Top', response.Message , 5);
        makeElementEnabled($('.save-repreq-btn'), 'حفظ');
      },
    });
  });
  /* Add & Edit Statements */
  var repreq_statement_element = $('.statement-g3').html();
  $('.add-statement-field-button').on('click', function() {
    let RepReq_Count = parseInt($('input[name=ReReqs_Count]').val());
    for (let i = 0;i < RepReq_Count;i++) {
      $('.statement-g3').append(repreq_statement_element);
    }
  });
  /* Enter Data Forms */
  $('.add-form-table').on('click', function() {
    let tableName = $('select[name=Table_Name]').val();
    if (tableName == 'entering_drivers') {
      addEnterDriverForm();
    }
    else if (tableName == 'entering_stores') {
      addEnterStoreForm();
    }
    else if  (tableName == 'entering_parts_repairs') {
      addEnterPartForm();
    }
  });
  $('.add-table-field-button').on('click', function() {
    let tableName = $('select[name=Table_Name]').val();
    if (tableName == 'entering_drivers') {
      $('.table-form').append(enterDriverField);
    }
    else if (tableName == 'entering_stores') {
      $('.table-form').append(enterStoreField);
    }
    else if  (tableName == 'entering_parts_repairs') {
      $('.table-form').append(enterPartField);
    }
  });
  $('.enter-data-form').submit(function(e) {
    e.preventDefault();
    let $form      = $(this);
    let data       = $form.serialize();
    let csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    let entering   = $('select[name=Table_Name]').val();
    let url        = window.origin + '/mech_dep/enter_data/' + entering + '/';
    makeElementDisabled($('.save-btn'), 'جار الحفظ..');
    $.ajax({
      type    :'POST',
      url     : url,
      data    : data,
      success : function(response) {
        TemporaryToast('Success', 'AutoWidth', 'Top', response.Message , 5);
        $('.table-form :input').val('');
        makeElementEnabled($('.save-btn'), 'حفظ');
      },
      error   : function(response){
        TemporaryToast('Error', 'AutoWidth', 'Top', response.Message , 5);
        makeElementEnabled($('.save-btn'), 'حفظ');
      },
    });
  });
  /* --  Changing Repair Request Status -- */
  $('.change-repreq-status-form').submit(function(e) {
    e.preventDefault();
    let $form      = $(this);
    let data       = $form.serialize();
    let csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    let url        = $form.attr('action');
    makeElementDisabled($('.save-repreq-status-btn'), 'جار الحفظ..');
    $.ajax({
      type    :'POST',
      url     : url,
      data    : data,
      success : function(response) {
        if (response.Status){
          TemporaryToast('Success', 'AutoWidth', 'Top', response.Message , 5);
          $('input[name=RepReq_No]').val('');
          $('input[name=RepReq_Year]').val('');
          makeElementEnabled($('.save-repreq-status-btn'), 'حفظ');
        }
        else {
          TemporaryToast('Error', 'AutoWidth', 'Top', response.Message , 5);
          makeElementEnabled($('.save-repreq-status-btn'), 'حفظ');
        }
      },
      error   : function(response){
        console.log(response);
        TemporaryToast('Error', 'AutoWidth', 'Top', response.statusText , 5);
        makeElementEnabled($('.save-repreq-status-btn'), 'حفظ');
      },
    });
  });
  /* --- Viewing Data --- */
  /* ----- Viewing Data Filtering ----- */
  $('select[name=Table]').on('change', function() {
    let table = $('select[name=Table]').val();
    let url   = window.origin + '/mech_dep/getTableColumns/' + table + "/";
    $('select[name=Filter').html('');
    $.getJSON(url, function(response) {
      if (!response.Status) {
        let msg_toast = 'Error';
        TemporaryToast('Error', 'AutoWidth', 'Top', msg_toast , 8);
      }
      else {
        $('select[name=Filter').html('');
        let Data = response.Data;
        for (let i = 0;i < Data.Codes.length;i++) {
          let option_field = "<option value=\"" + Data.Codes[i] + "\"> " + Data.Names[i] + "</option>";
          $('select[name=Filter]').append(option_field);
        }
      }
    });
  })
  $('select[name=Filter]').on('change', function() {
    let table  = $('select[name=Table]').val(); 
    let column = $('select[name=Filter]').val();
    let url    = window.origin + '/mech_dep/getColumnValues/' + table + "/" + column + "/";
    $('select[name=Keyword').html('');
    $.getJSON(url, function(response) {
      if (!response.Status) {
        let msg_toast = 'Error';
        TemporaryToast('Error', 'AutoWidth', 'Top', msg_toast , 8);
      }
      else {
        $('select[name=Keyword').html('');
        let Data = response.Data;
        for (let i = 0;i < Data.length;i++) {
          let option_field = "<option value=\"" + Data[i] + "\"> " + Data[i] + "</option>";
          $('select[name=Keyword]').append(option_field);
        }
      }
    });
  });
  $('select[name=Keyword]').on('change', function() {
    let table   = $('select[name=Table]').val(); 
    let url     = window.origin + '/mech_dep/getColumnValues/' + table + "/Year/";
    $('select[name=Year').html('');
    $.getJSON(url, function(response) {
      if (!response.Status) {
        let msg_toast = 'Error';
        TemporaryToast('Error', 'AutoWidth', 'Top', msg_toast , 8);
      }
      else {
        $('select[name=Year').html('');
        let Data = response.Data;
        for (let i = 0;i < Data.length;i++) {
          let option_field = "<option value=\"" + Data[i] + "\"> " + Data[i] + "</option>";
          $('select[name=Year]').append(option_field);
        }
      }
    });
  });
  $('select[name=Keyword]').on('click', function() {
    let table   = $('select[name=Table]').val(); 
    let url     = window.origin + '/mech_dep/getColumnValues/' + table + "/Year/";
    $('select[name=Year').html('');
    $.getJSON(url, function(response) {
      if (!response.Status) {
        let msg_toast = 'Error';
        TemporaryToast('Error', 'AutoWidth', 'Top', msg_toast , 8);
      }
      else {
        $('select[name=Year').html('');
        let Data = response.Data;
        for (let i = 0;i < Data.length;i++) {
          let option_field = "<option value=\"" + Data[i] + "\"> " + Data[i] + "</option>";
          $('select[name=Year]').append(option_field);
        }
      }
    });
  });
  $('.view-data-filtering').on('click', function() {
    let DataModel = $('select[name=Table]').val();
    let Filter    = $('select[name=Filter]').val();
    let Keyword   = $('select[name=Keyword]').val();
    let Year      = $('select[name=Year]').val();
    console.log(DataModel + "---" + Filter + "---" + Keyword);
    let url       = window.origin + "/mech_dep/view_data/data_filtering/" + DataModel + "/" + Filter + "/" + Keyword + "/" + Year + "/";
    window.open(url, '_blank');
  });
  /* ---- Balances Pages ---- */
  /* -- Setting SubBalances / Add SubBalance Field -- */
  var subBalanceElement = $('.sub-balance-inputs').html();
  $('.add-sub-balance-field').on('click', function() {
    $('.sub-balance-inputs').append(subBalanceElement);
  });
  $('.sub-balance-form').submit(function(e) {
    e.preventDefault();
    let $form      = $(this);
    let data       = $form.serialize();
    let url        = $form.attr('action');
    makeElementDisabled($('.save-btn '), 'جار الحفظ..');
    $.ajax({
      type    :'POST',
      url     : url,
      data    : data,
      success : function(response) {
        if (response.Status) {
          TemporaryToast('Success', 'AutoWidth', 'Top', response.Message , 5);
          $('.sub-balance-inputs :input').val('');
          makeElementEnabled($('.save-btn'), 'حفظ');
        }
        else {
          TemporaryToast('Error', 'AutoWidth', 'Top', response.Message , 5);
          makeElementEnabled($('.save-btn'), 'حفظ');
        }
      },
      error   : function(response){
        TemporaryToast('Error', 'AutoWidth', 'Top', 'error' , 5);
        makeElementEnabled($('.save-btn'), 'حفظ');
      }
  });
})
  /* -- Setting SubBalances Items / Add SubBalance Items Field -- */
  var subBalanceItemElement = $('.sub-balance-item-inputs').html();
  $('.add-subbalance-item-field').on('click', function() {
    $('.sub-balance-item-inputs').append(subBalanceItemElement);
  });
  $('.sub-balance-item-form').submit(function(e) {
    e.preventDefault();
    let $form      = $(this);
    let data       = $form.serialize();
    let url        = $form.attr('action');
    makeElementDisabled($('.save-btn '), 'جار الحفظ..');
    $.ajax({
      type    :'POST',
      url     : url,
      data    : data,
      success : function(response) {
        if (response.Status) {
          TemporaryToast('Success', 'AutoWidth', 'Top', response.Message , 5);
          $('.sub-balance-item-inputs :input').val('');
          makeElementEnabled($('.save-btn'), 'حفظ');
        }
        else {
          TemporaryToast('Error', 'AutoWidth', 'Top', response.Message , 5);
          makeElementEnabled($('.save-btn'), 'حفظ');
        }
      },
      error   : function(response){
        TemporaryToast('Error', 'AutoWidth', 'Top', response.Message , 5);
        makeElementEnabled($('.save-btn'), 'حفظ');
      },
  });
})
  /* Check & Validate using Ajax Functions */
  /* -- Checking Mechanism ID -- */
  var mechIDTypingTimer;
  var mechIDTypingInterval = 3000;
  var $mech_id_input = $('#Mech-ID');
  $mech_id_input.on('change', function () {
    clearTimeout(mechIDTypingTimer);
    mechIDTypingTimer = setTimeout(mechIDTyping, mechIDTypingInterval);
  });
  $mech_id_input.on('keydown', function () {
    clearTimeout(mechIDTypingTimer);
  });
  function mechIDTyping () {
    if ($mech_id_input.val().length > 4) {
      let mech_id = $mech_id_input.val()
      let url = window.origin + "/mech_dep/getMechData/" + mech_id + "/";
      $.getJSON(url, function(response) {
        if (!response.Status) {
          $mech_id_input.css('border', '2px solid red');
          let msg_toast = response.Message;
          TemporaryToast('Error', 'Large', 'Top', msg_toast , 5);
        }
        else {
          $mech_id_input.css('border', '3px solid lime');
          $('#Mech-Model').text('نوع السيارة : ' + response.Model);
          $('#Mech-Ownership').text('العائدية : ' + response.Ownership);
          $('#Mech-Disposal').text('تحت تصرف : ' + response.Disposal);
        };
      });
    };
  };
  /* -- Checking Repair Request ID -- */
  var dateTypingTimer;
  var reqNoTypingTimer;
  var dateTypingInterval = 3000;
  var $date_input        = $('input[name=Req_Date]');
  var $req_no_input      = $('input[name=Req_No]');
  $date_input.on('change', function () {
    clearTimeout(dateTypingTimer);
    dateTypingTimer = setTimeout(dateTyping, dateTypingInterval);
  });
  $req_no_input.on('change', function () {
    clearTimeout(reqNoTypingTimer);
    reqNoTypingTimer = setTimeout(dateTyping, dateTypingInterval);
  });
  $date_input.on('keydown', function () {
    clearTimeout(dateTypingTimer);
  });
  $req_no_input.on('keydown', function () {
    clearTimeout(reqNoTypingTimer);
  });
  function dateTyping () {
    if ($date_input.val().length > 4) {
      let repreq_no = $req_no_input.val();
      let year      = $date_input.val().split('-')[0]
      let repreq_id = repreq_no + "_" + year;
      let url = window.origin + "/mech_dep/checkRepairRequestID/" + repreq_id + "/";
      $.getJSON(url, function(response) {
        if (!response.Status) {
          $date_input.css('border', '2px solid red');
          $req_no_input.css('border', '2px solid red');
          let msg_toast = response.Message;
          TemporaryToast('Error', 'Large', 'Top', msg_toast , 5);
        }
        else {
          $date_input.css('border', '2px solid lime');
          $req_no_input.css('border', '2px solid lime');
        }
      });
    };
  };
});
