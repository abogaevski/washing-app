var config = {
    select: true,
    "order": [
        [0, "desc"]
    ],
    "language": {
        "lengthMenu": "_MENU_",
        "zeroRecords": "Ничего не найдено",
        "info": "Страниц: _PAGE_ из _PAGES_",
        "zeroRecords": "Записей нет",
        "infoEmpty": "Не найдено",
        "infoFiltered": "(Поиск по _MAX_ записям)",
        "search": "Фильтр",
        "paginate": {
            "first": "Первая",
            "last": "Последняя",
            "next": "Следующая",
            "previous": "Предыдущая"
        },
    },
    destroy: false,
    orderCellsTop: true,
}

function getDetailForEntity(item, url) {
    itemID = $(item).data('itemId')
    csrftoken = $(item).find('input[name=csrfmiddlewaretoken]').val()
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'itemid': itemID
        },
        success: function(data) {
            $('.details').html(data);
            $(".background-overlay").addClass("active");
            $("body").css("overflow", "hidden");
            setTimeout(function() {
                $(".details").addClass("active"), 1000
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

function addCoinsHandle(url) {
    $('form input').keydown(function(e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });

    $('button[data-item-id]').click(function() {
        csrf = $(document).find('input[name=csrfmiddlewaretoken]').val();
        item = $(this).data('itemId');
        balance = $('input#id_balance_' + item).val();
        addCoinsForPartner(csrf, item, balance, url);
    });
}

function closeModal() {
    $(".slider-close").click(function() {
        $(".background-overlay").removeClass("active");
        $(".details").removeClass("active");
        $("body").css("overflow", "unset");
    });

    $(document).keydown(function(e) {
        if (e.keyCode == 27) {
            $(".background-overlay").removeClass("active");
            $(".details").removeClass("active");
            $("body").css("overflow", "unset");
        }
    });

    $(".background-overlay").click(function() {
        $(".background-overlay").removeClass("active");
        $(".details").removeClass("active");
        $("body").css("overflow", "unset");
    });
}

$(".nav-item [data-toggle]").click(function() {
    $(this).find("i.fas").toggleClass("fa-sort-down", "fa-sort-up")
})