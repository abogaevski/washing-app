table = dataTable('.table-transactions', config);
  
    $.fn.dataTable.ext.search.push(
        function (settings, data, dataIndex) {
            var min = $('#min').datepicker("getDate");
            var max = $('#max').datepicker("getDate");
            // console.log($.datepicker.formatDate('dd.mm.yy', min))
            splitDate = data[5].split(' ')
            splitDate = splitDate[0].split('.')
            // console.log(splitDate)
            var startDate = new Date(splitDate[1] + '.' + splitDate[0] + '.' + splitDate[2]);
            // console.log(startDate)
           
            if (min == null && max == null) { return true; }
            if (min == null && startDate <= max) { return true;}
            if(max == null && startDate >= min) {return true;}
            if (startDate <= max && startDate >= min) { return true; }
            return false;
        }
    );
