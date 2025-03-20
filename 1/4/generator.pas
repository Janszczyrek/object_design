program generator;
uses Math;


const count = 10;

procedure Generate(var arr: Array of Integer; var start: Integer; var stop: Integer);
var i: Integer;
begin
  Randomize;
  for i := 0 to count-1 do arr[i] := RandomRange(start,stop+1)
end;

var
  i, start, stop: Integer;
  arr: Array[0..count-1] of Integer;

begin
start := -100;
stop := 100;
Generate(arr,start,stop);
for i := 0 to count-1 do Write(arr[i], ', ');
WriteLn();
end.