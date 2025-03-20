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

procedure Generate(var arr: Array of Integer);
var i: Integer;
begin
    Randomize;
    for i := 0 to count-1 do arr[i] := RandomRange(0,101);
end;

var
    i: Integer;
    arr: Array[0..49] of Integer;

begin
    Generate(arr);
    for i := 0 to count-1 do Write(arr[i], ', ');
    WriteLn();
    Sort(arr);
    for i := 0 to count-1 do Write(arr[i], ', ');
    WriteLn();
end.