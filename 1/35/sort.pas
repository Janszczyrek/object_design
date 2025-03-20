program sort;
uses Math;

const count = 10;


procedure Sort(var arr: Array of Integer);
var
  i, j, temp: Integer;
begin
  for i := 0 to count-1 do
  begin
    for j := count-1 downTo i do
    begin
      if arr[j-1] > arr[j] then
      begin
        temp := arr[j];
        arr[j] := arr[j-1];
        arr[j-1] := temp;
      end;
    end;
  end;
end;

var
  i: Integer;
  arr: Array[0..9] of Integer = (-1, 100, 90, -30, 20, 24, -23, 32, -13, 16);

begin
  
  for i := 0 to count-1 do Write(arr[i], ', ');
  WriteLn();
  Sort(arr);
  for i := 0 to count-1 do Write(arr[i], ', ');
  WriteLn();
end.