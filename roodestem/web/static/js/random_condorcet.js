$(function() {
  var candidateTable = $('#candidate_table');
  var i = $('#candidate_table tr').length + 2;
        
  $('#add_candidate').on('click', null, function() {
    if(i == 100){
      return;
    }
    $('<tr><td><label for="candidates-' + i+ '">Candidate</label>:</td><td><input class="form-control" id="candidates-1" name="candidates-' + i+ '" type="text" value=""></td><td><button type="button" class="btn btn-default btn-sm" id="remove_candidate"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button></td></tr>').appendTo(candidateTable);
    i++;
    return false;
  });
        
  $('#remove_candidate').on('click', null, function() { 
    $(this).parents('td').remove();
    i--;
    return false;
  });
});
