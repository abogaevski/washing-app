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
    orderCellsTop: true,
}

$(document).ready(function () {

    $('.table-list thead tr').clone(true).appendTo( '.table-list thead' );
    $('.table-list thead tr:eq(1) th').each( function (i) {

        if ( $(this).data().hasOwnProperty("filterable") ) {
            var title = $(this).text();
            $(this).html( '<div class="input-group input-group-sm"><input class="form-control" type="text" placeholder="Найти '+title+'" /></div>' );
        } else {
            $(this).html(" ");
        }
       
 
        $( 'input', this ).on( 'keyup change', function () {
            if ( table.column(i).search() !== this.value ) {
                table
                    .column(i)
                    .search( this.value )
                    .draw();
            }
        } );
    } );
    
    table = dataTable('.table-list', config);

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
            $('.detail-container').hide();
            $('.detail-container').html(data);
            setTimeout(function () {
                $('.detail-container').fadeIn('slow'), 1000
            });
            var table = dataTable('.table-transactions', config);
        }
    });
}

function dataTable(table, config) {
    table = $(table).DataTable(
        config
    );
    return table 
    
}

