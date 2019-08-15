var config = {
    select: true,
    "order": [[ 0, "desc" ]],
    "language": {
        "lengthMenu": "_MENU_",
        "zeroRecords": "Ничего не найдено",
        "info": "Страниц: _PAGE_ из _PAGES_",
        "zeroRecords":    "Записей нет",
        "infoEmpty": "Не найдено",
        "infoFiltered": "(Поиск по _MAX_ записям)",
        "search" : "Фильтр",
        "paginate": {
            "first":      "Первая",
            "last":       "Последняя",
            "next":       "Следующая",
            "previous":   "Предыдущая"
        },
    },
    destroy: false,   
}

$(document).ready(function () {
    
    table = dataTable('.table-list', config);

    $.fn.dataTable.ext.search.push(
        function (settings, data, dataIndex) {
            var min = $('#min').datepicker("getDate");
            var max = $('#max').datepicker("getDate");
            splitDate = data[5].split(' ')
            splitDate = splitDate[0].split('.')
            // var start = Date(splitDate[0]);
            startDate = new Date(parseInt(splitDate[2]), parseInt(splitDate[1]) - 1, parseInt(splitDate[0]));
                       
            if (min == null && max == null) { return true; }
            if (min == null && startDate <= max) { return true;}
            if(max == null && startDate >= min) {return true;}
            if (startDate <= max && startDate >= min) { return true; }
            return false;
        }
    );

    $("#min").datepicker({ onSelect: function () { table.draw(); }, changeMonth: true, changeYear: true });
    $("#max").datepicker({ onSelect: function () { table.draw(); }, changeMonth: true, changeYear: true });

    //   // Event listener to the two range filtering inputs to redraw on input
    $('#min, #max').change(function () {
        table.draw();
    });


});

function getDetailForEntity(item, url) {
    // elem = $(item).find('[data-item-id]')
    itemID = $(item).data('itemId')
    csrftoken = $(item).find('input[name=csrfmiddlewaretoken]').val()
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'itemid': itemID
        },
        success: function (data) {
            $('.detail-container').hide()
            $('.detail-container').html(data)
            setTimeout(function () {
                $('.detail-container').fadeIn('slow'), 1000
            });
            var table = dataTable('.table-transactions', config);


            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    var min = $('#min').datepicker("getDate");
                    var max = $('#max').datepicker("getDate");
                    // console.log($.datepicker.formatDate('dd.mm.yy', min))
                    splitDate = data[5].split(' ')
                    splitDate = splitDate[0].split('.')
                    startDate = new Date(parseInt(splitDate[2]), parseInt(splitDate[1]) - 1, parseInt(splitDate[0]));
                   
                    if (min == null && max == null) { return true; }
                    if (min == null && startDate <= max) { return true;}
                    if(max == null && startDate >= min) {return true;}
                    if (startDate <= max && startDate >= min) { return true; }
                    return false;
                }
            );
      
            $("#min").datepicker({ onSelect: function () { table.draw(); }, changeMonth: true, changeYear: true });
            $("#max").datepicker({ onSelect: function () { table.draw(); }, changeMonth: true, changeYear: true });
    
            //   // Event listener to the two range filtering inputs to redraw on input
              $('#min, #max').change(function () {
                  table.draw();
              });
                        
        }
    });
}

function dataTable(table, config) {
    table = $(table).DataTable(
        config
    );
    return table 
    
}

