/* General Functions */
function makeElementDisabled(element, text) {
  element.prop('disabled', true);
  element.addClass('Disabled');
  element.val(text);
};
function makeElementEnabled(element, text) {
  element.prop('disabled', false);
  element.removeClass('Disabled');
  element.val(text);
}
/* Toasts Functions */
function TemporaryToast(Type, Size, Alignment, Message, Seconds) {
  var toastElement = "<div class=\"TemporaryToast " + " Toast-" + Type + " Toast-" + Size + " Toast-" + Alignment + "\">\
                      <p class=\"ToastText\">" + Message + "</p> </div> </div>";
  $('body').append(toastElement);
  window.setTimeout(function() {
    $('.TemporaryToast').remove();
  }, Seconds*1000);
};

function CloseableToast(Type, Size, Alignment, Message) {
  var toastElement = "<div class=\"CloseableToast" + " Toast-" + Type + " Toast-" + Size + " Toast-" + Alignment + "\">\
                      <span class=\"CloseToast\">&times;</span> <div class=\"ToastContent\">\
                      <p class=\"ToastText\">" + Message + "</p> </div> </div>";
  $('body').append(toastElement);
  $('.CloseToast').click(function() {
    $('.CloseableToast').remove();
  });
};

/* Editing RepairRequest / RepairsDetails & Deleting RepairsDetails -> Functions */
function editRepairRequestData(Data) {
  $('.edit-repreqdata-form input[name=Mech_ID]').val(Data.Mech_ID);
  $('.edit-repreqdata-form input[name=Req_Date]').val(Data.Req_Date);
  $('.edit-repreqdata-form input[name=Kilometers]').val(Data.Kilometers);
  $('.edit-repreqdata-form input[name=Driver_Name]').val(Data.Driver_Name);
  $('.edit-repreqdata-form input[name=Real_Cost]').val(Data.Real_Cost);
  $('.edit-repreqdata-form input[name=Rep_Type]').val(Data.Repir_Type);
  $('.edit-repreqdata-form input[name=Receipt_Date]').val(Data.Receipt_Date);
  $('.edit-repreqdata-form input[name=Expected_Cost]').val(Data.Expected_Cost);
  $('.edit-repreqdata-form input[name=Approval]').val(Data.Approval);
  $('.editdetails-form').hide();
  $('.edit-repreqdata-form').show();
  $('.edit-repreq-btn').show();
}

function editRepairsDetails(Data) {
  let g3Elements = $('.repreq-g3-edit-container').html()
  for (let i = 0; i < Data.length-1; i++) {
    $('.repreq-g3-edit-container').append(g3Elements);
  };
  for (let i = 0; i < Data.length; i++) {
    $('input[name=Repair_ID]')[i].value  = Data[i].id;
    $('input[name=Repairs]')[i].value    = Data[i].Part_Repair;
    $('input[name=Quantity]')[i].value   = Data[i].Part_Count;
    $('input[name=Type]')[i].value       = Data[i].Part_Type;
    $('input[name=Cost]')[i].value       = Data[i].Cost;
    $('input[name=Receipt_No]')[i].value = Data[i].Receipt_No;
    $('input[name=Store_Name]')[i].value = Data[i].Store;
  };
  $('.editdetails-form').hide();
  $('.edit-repairsdetails-form').show();
  $('.edit-repreq-btn').show();
};

function deleteRepairsDetails(Data) {
  let g3ElementsD = $('.repreq-g3-container-d').html()
  for (let i = 0; i < Data.length-1; i++) {
    $('.repreq-g3-container-d').append(g3ElementsD);
  };
  for (let i = 0; i < Data.length; i++) {
    $('input[name=D_Repair_ID]')[i].value    = Data[i].id;
    $('input[name=D_Repairs]')[i].value      = Data[i].Part_Repair;
    $('input[name=D_Quantity]')[i].value     = Data[i].Part_Count;
    $('input[name=D_Type]')[i].value         = Data[i].Part_Type;
    $('input[name=D_Cost]')[i].value         = Data[i].Cost;
    $('.delete-repair-button')[i].className += " del-rep-id-" + Data[i].id;
  };
  $('.editdetails-form').hide();
  $('.delete-repairsdetails-form').show();
};

function deleteRepair(element) {
  let cls    = element.className.split(' ');
  let rep_id = cls[1].split('-')[3];
  let url    = window.origin + "/mech_dep/deleting_mechrep/" + rep_id + "/";
  alert(cls, rep_id);
  $.getJSON(url, function(data) {
    if (!data.Status) {
      let msg_toast = data.Message;
      TemporaryToast('Error', 'AutoWidth', 'Top', msg_toast, 5);
    }
    else {
      let msg_toast = data.Message;
      TemporaryToast('Success', 'AutoWidth', 'Top', msg_toast, 5);
      makeElementDisabled($(element), 'محذوف');
    }
  });
};

/* Add & Edit Receipts */
function Add_Receipt(Data) {
  let g3Elements = $('.receipt-g3').html()
  for (let i = 0; i < Data.length-1; i++) {
    $('.receipt-g3-container').append('<div class="receipt-g3">' + g3Elements + '</div>');
  };
  $('.receipt-g3-container').show();
  for (let i = 0; i < Data.length; i++) {
    $('input[name=Repair_ID]')[i].value  = Data[i].id;
    $('input[name=Repairs]')[i].value    = Data[i].Part_Repair;
    $('input[name=Quantity]')[i].value   = Data[i].Part_Count;
    $('input[name=Type]')[i].value       = Data[i].Part_Type;
    $('input[name=Cost]')[i].value       = Data[i].Cost;
    $('input[name=Receipt_No]')[i].value = Data[i].Receipt_No;
    $('input[name=Store_Name]')[i].value = Data[i].Store;
  };
  $('.receipt-g1').hide();
  $('.receipt-g2-container').show();
  $('.add-receipt-button').show();
  $('.receipt-g3-container').show();
  $('.save-receipt-btn').show();
};

function Edit_Receipt(Data) {
  true;
};

/* Enter Data Forms */
var enterDriverField = '<div class="drivers-table-field flex-row space-around my-10 rtl w-90 ">' + $('.drivers-table-field').html() +'</div>';
var enterStoreField  = '<div class="stores-table-field flex-row space-around my-10 rtl w-90 ">' + $('.stores-table-field').html() + '</div>';
var enterPartField   = '<div class="parts-table-field flex-row space-around my-10 rtl w-90 ">' + $('.parts-table-field').html() + '</div>';
/* Add Driver Form */
function addEnterDriverForm() {
  $('select[name=Table_Name]').prop('disabled', true);
  $('.add-form-table').hide();
  $('.table-form').html(enterDriverField);
  $('.table-form').show();
  $('.add-table-field-button').show();
  $('.save-btn').show();
}
/* Add Store Form */
function addEnterStoreForm() {
  $('select[name=Table_Name]').prop('disabled', true);
  $('.add-form-table').hide();
  $('.table-form').html(enterStoreField);
  $('.table-form').show();
  $('.add-table-field-button').show();
  $('.save-btn').show();
}
/* Add Parts and Repairs Form */
function addEnterPartForm() {
  $('select[name=Table_Name]').prop('disabled', true);
  $('.add-form-table').hide();
  $('.table-form').html(enterPartField);
  $('.table-form').show();
  $('.add-table-field-button').show();
  $('.save-btn').show();
}
