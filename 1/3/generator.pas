program generator;
uses Math;


procedure Generate(var arr: Array of Integer);
var i: Integer;
begin
    Randomize;
    for i := 0 to 49 do arr[i] := RandomRange(0,101);
end;

var
    i: Integer;
    arr: Array[0..49] of Integer;
begin

    Generate(arr);
    for i := 0 to 49 do Write(arr[i], ', ');
    WriteLn();
end.