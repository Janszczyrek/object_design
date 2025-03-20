program generator;
uses Math;


procedure Generate();
var i: Integer;
begin
  Randomize;
  for i := 1 to 50 do Write(RandomRange(0,101), ', ');
end;

begin
Generate();
WriteLn();
end.