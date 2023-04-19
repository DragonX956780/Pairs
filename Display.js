function alert(){
    window.alert("Hi");
}

test.ajax({
  type: "POST",
  url: "Backtesting.py",
  data: { param: text}
}).done(function( o ) {
   // do something
});