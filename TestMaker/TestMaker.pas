uses crt, GraphABC;
type que=record
  question:string;
  answ:string;
end;
type logicForm=record
  form:string;
  sForm:string;
end;
type logicTable=record
  size:integer;
  table:array of logicForm;
  ind:integer;
  procedure setSize(s:integer);
  begin
    ind:=0;
    size:=s;
    setLength(table,s);
  end;
  procedure add(s1:string; s2:string);
  begin
    if(ind<size)then 
    begin
      table[ind].form:=s1;
      table[ind].sForm:=s2;
      ind:=ind+1;
    end;
  end;
end;
type PicTask=record
  task:que;
  pic:Picture;
end;

procedure write(q:que);
begin
  writeln(q.question);
  write(q.answ);
end;
procedure writeln(q:que);
begin
  write(q);
  writeln();
end;

function from10(x:integer; deg:integer):string;
var
  t:integer;
  rs:string;
begin
  while(x>0)do
  begin
    t:=x mod deg;
    if(t>=10)then
      rs:=chr(ord('A')+t-10)+rs
    else
      rs:=chr(ord('0')+t)+rs;
    x:=x div deg;
  end;
  from10:=rs;
end;
function to10(s:string; deg:integer):integer;
var
  rs:integer;
begin
  rs:=0;
  while(length(s)>0)do
  begin
    rs:=rs*deg;
    if (ord(s[1])-ord('0')<=9) then
      rs:=rs+(ord(s[1])-ord('0'))
    else
      rs:=rs+(ord(s[1])-ord('A'))+10;
    s:=s.Remove(0,1);
  end;
  to10:=rs;
end;


function qu_1_1(num:integer):que;
var
  x,y:integer;
  res:que;
begin
  x:=(num mod 23)+11;
  x:=x * x +11;
  x:=(x mod 31) +17;
  y:=(num mod 5)+4;
  res.question:='Переведите число '+IntToStr(x)+' из десятичной в '+ IntToStr(y)+'-ричную';
  res.answ:=from10(x,y);
  qu_1_1:=res;
end;

function qu_1_2(num:integer):que;
var
  x,y:integer;
  res:que;
begin
  x:=(num mod 31)+7;
  x:=x * x +13;
  x:=(x mod 43) +19;
  y:=(num mod 7)+3;
  res.question:='Переведите число '+from10(x,y)+' из '+ IntToStr(y)+'-ричной в десятичную';
  res.answ:=IntToStr(x);
  qu_1_2:=res;
end;
function Qu1(num:integer):que;
begin
  if(num mod 2)=0 then
    Qu1:=qu_1_1(num)
  else
    Qu1:=qu_1_2(num);
end;
function qu_2_1(num:integer):que;
var
  x,y1,y2:integer;
  res:que;
begin
  y1:=num mod 31;
  y1:=(y1+3)*(y1+5)*(y1+7);
  y1:=(y1 mod 4)+2;
  if(y1=2)then y2:=(num mod 3)+2
  else
    if(y1=3) then y2:=(num mod 2)+2
    else
      y2:=2;
  x:=(num mod 47)+13;
  x:=(x+13)*(x div 4);
  if(x<400) then x:=(x mod 641)
  else x:=x-239;
  res.question:='Переведите число '+from10(x,y1)+' из '+ IntToStr(y1)+'-ричной в '+IntToStr(floor(Power(y1,y2)));
  res.answ:=from10(x,floor(Power(y1,y2)));
  qu_2_1:=res;
end;
function qu_2_2(num:integer):que;
var
  x,y1,y2:integer;
  res:que;
begin
  y1:=(num mod 43)+17;
  y1:=y1*y1;
  y1:=(y1 mod 7)+2;
  y2:=(num mod 2)+2;
  if(y1>5)and(y2=3) then y2:=2;
  x:=(num mod 101)+17;
  x:=x*x;
  x:=(x mod 119)+(num mod 7)+3;
  res.question:='Переведите число '+from10(x,floor(Power(y1,y2)))+' из '+ IntToStr(floor(Power(y1,y2)))+'-ричной в '+IntToStr(y1);
  res.answ:=from10(x,y1);
  qu_2_2:=res;
end;
function Qu2(num:integer):que;
begin
  if(num mod 2)=0 then
    Qu2:=qu_2_1(num)
  else
    Qu2:=qu_2_2(num);
end;

function wayPoint(tbl:array of array of integer; size:integer):integer;
var
  ways:array of integer;
  posWays:array of integer;
  find:boolean;
  x,y,i,mn,mnInd:integer;
begin
  setLength(ways,size);
  setLength(posWays,size);
  for i:=0 to size-1 do
  begin
    posWays[i]:=-1;
    ways[i]:=-1;
  end;
  ways[0]:=0;
  find:=true;
  y:=0;
  while(find)do
  begin
    for x:=0 to size-1 do
    begin
      if(ways[x]=-1)and(tbl[x][y]>0)and((ways[y]+tbl[x][y]<posWays[x])or(posWays[x]=-1))then
        posWays[x]:=ways[y]+tbl[x][y];
    end;
    mnInd:=-1;
    mn:=-2;
    find:=false;
    for i:=0 to size-1 do
    begin
      if(posWays[i]>=0)then
      begin
        find:=true;
        if(mnInd=-1)or(mn>posWays[i])then
        begin
          mn:=posWays[i];
          mnInd:=i;
        end;
      end;
    end;
    if(find)then
    begin
      posWays[mnInd]:=-1;
      ways[mnInd]:=mn;
      y:=mnInd;
    end;
  end;
  wayPoint:=ways[size-1];
end;
function Qu3(num:integer):que;
var
  res:que;
  tbl:array of array of integer;
  size,i,x,y,tp,dl:integer;
begin
  randomize(num);
  size:=((num mod 7)+11)div 2;
  setlength(tbl,size);
  for i:=0 to size-1 do
    setLength(tbl[i],size);
  res.question:='Найдите кратчайший путь из вершины А в вершину '+chr(ord('A')+size-1)+chr(10);
  tp:=(num mod 101)+87;
  i:=0;
  while(wayPoint(tbl,size)=-1)or(i<(3*size))do
  begin
    x:=(tp+((num*i)mod 5)+random(size)) mod size;
    y:=(tp+((num*i)mod 7)+random(size)) mod size;
    if(x=y)then y:=(y+1)mod size;
    dl:=(tp mod 7)+(tp mod 3)+1;
    if(((x+size-2) mod size>(size-4))and(x=(size-1))or((x+size-2) mod size>(size-4))and(y=(size-1)))and(dl<7)then
      dl:=dl+7;
    if(dl=0)then dl:=1;
    tbl[x][y]:=dl;
    tbl[y][x]:=dl;
    tp:=tp+13;
    if(wayPoint(tbl,size)<>-1)then i:=i+1;
  end;
  res.answ:=IntToStr(wayPoint(tbl,size));
  res.question:=res.question+' '+chr(9);
  for y:=0 to size-1 do
    res.question:=res.question+chr(ord('A')+y)+chr(9);
  res.question:=res.question+chr(10);    
  for y:=0 to size-1 do
  begin
    res.question:=res.question+chr(ord('A')+y)+chr(9);
    for x:=0 to size-1 do
      if(tbl[x][y]<>0)then
        res.question:=res.question+IntToStr(tbl[x][y])+chr(9)
      else
        res.question:=res.question+'X'+chr(9);
    if(y<size-1)then
      res.question:=res.question+chr(10);
  end;
  Qu3:=res;
end;

function qu_4_1_ex(num:integer):que;
var
  itter:integer;
  s:string;
  tb:logicTable;
  kol,find:integer;
  res:que;
begin
    case (num mod 8) of
    0:s:='A&B';
    1:s:='A&!B';
    2:s:='!A&B';
    3:s:='AVB';
    4:s:='AV!B';
    5:s:='!AVB';
    6:s:='A';
    7:s:='B';
  end;
  res.answ:=s;
  tb.setSize(8);
  tb.add('(A&(AVB))','A');
  tb.add('(A&0)','0');
  tb.add('(A&1)','A');
  tb.add('!(A&B)','!AV!B');
  tb.add('(AV1)','1');
  tb.add('(AV(A&B))','A');
  tb.add('(!(AVB))','!A&!B');
  tb.add('(AV0)','A');
  itter:=num mod 7;
  itter:=itter+3;
  kol:=0;
  while(itter<>0)do
  begin
    find:=-1;
    while(find=-1)do
    begin
      find:=s.IndexOf(tb.table[kol].sForm,0,length(s));
      if(find<>-1)then break;
      kol:=(kol+1) mod tb.size;
    end;
    s:=s.Remove(find,1);
    s:=s.Insert(find,tb.table[kol].form);
    itter:=itter-1;
    kol:=(kol+1) mod tb.size;
  end;
  res.question:=s;
  qu_4_1_ex:=res;
end;
function qu_4_1(num:integer):que;
var
  s:string;
  res:que;
begin
  res:=qu_4_1_ex(num);
  res.question:='Сократите выражение:'+chr(10)+res.question;
  qu_4_1:=res;
end;
function qu_4_2_ex(num:integer):que;
var
  itter:integer;
  s:string;
  tb:logicTable;
  kol,find:integer;
  res:que;
begin
    case (num mod 11) of
    0:s:='A&B';
    1:s:='A&!B';
    2:s:='!A&B';
    3:s:='A&C';
    4:s:='AVB';
    5:s:='AV!B';
    6:s:='!AVB';
    7:s:='AVC';
    8:s:='A';
    9:s:='B';
    10:s:='C';
  end;
  res.answ:=s;
  tb.setSize(10);
  tb.add('!(A&B)','!AV!B');
  tb.add('A&(AVB)','A');
  tb.add('B&(BVC)','B');
  tb.add('!(A&C)','!AV!C');
  tb.add('!(A&B)','!AV!B');
  tb.add('(AV(A&B))','A');
  tb.add('(CV(C&B))','C');
  tb.add('C&(AVB)','A&CVB&C');
  tb.add('!(AVB)','!A&!B');
  tb.add('!(AVC)','!A&!C');
  itter:=num mod 5;
  itter:=itter+5;
  kol:=0;
  while(itter<>0)do
  begin
    find:=-1;
    while(find=-1)do
    begin
      find:=s.IndexOf(tb.table[kol].sForm,0,length(s));
      if(find<>-1)then break;
      kol:=(kol+1) mod tb.size;
    end;
    s:=s.Remove(find,1);
    s:=s.Insert(find,tb.table[kol].form);
    itter:=itter-1;
    kol:=(kol+1) mod tb.size;
  end;
  res.question:=s;
  qu_4_2_ex:=res;
end;
function qu_4_2(num:integer):que;
var
  res:que;
begin
  res:=qu_4_2_ex(num);
  res.question:='Сократите выражение:'+chr(10)+res.question;
  qu_4_2:=res;
end;
function Qu4(num:integer):que;
begin
  num:=num mod 11;
  if(num mod 2)=0 then
    Qu4:=qu_4_1(num)
  else
    Qu4:=qu_4_2(num);
end;

function Qu5(num:integer):que;
var
  z1,z2,z3:integer;
  res:que;
  tabl:array of array [0..1] of string;
begin
  z1:=(num mod 101)+7;
  z1:=z1*z1*z1;
  z1:=(z1 mod 503)+37;
  z2:=(num mod 89)+11;
  z2:=z1*(z1+7);
  z2:=(z1 mod 503)+163;
  z3:=(num mod 67)+41;
  z3:=(z1+7)*(z1+5)*(z1+3);
  z3:=(z1 mod 661)+179;
  setLength(tabl,6);
  tabl[0][0]:='Пчелы';    tabl[0][1]:='Медведи';
  tabl[1][0]:='Пчелы';    tabl[1][1]:='Мед';
  tabl[2][0]:='Море';     tabl[2][1]:='Картины';
  tabl[3][0]:='Гроза';    tabl[3][1]:='Вспышка';
  tabl[4][0]:='Реферат';  tabl[4][1]:='Математика';
  tabl[5][0]:='Парты';    tabl[5][1]:='Учебный класс';
  res.question:='Найдите количество результатов поискового запроса (в тысячах) "';
  case (num mod 3) of
    0:begin
        res.question:=res.question+tabl[num mod length(tabl)][0]+'"&"'+tabl[num mod length(tabl)][1]+
          '", если известны результаты следующих поисковых запросов:'+chr(10)+
          chr(9)+'* "'+tabl[num mod length(tabl)][0]+'" - '+IntToStr(z1+z2)+' тыс. результатов'+chr(10)+
          chr(9)+'* "'+tabl[num mod length(tabl)][1]+'" - '+IntToStr(z2+z3)+' тыс. результатов'+chr(10)+
          chr(9)+'* "'+tabl[num mod length(tabl)][0]+'"V"'+tabl[num mod length(tabl)][1]+'" - '+IntToStr(z1+z2+z3)+' тыс. результатов';
          res.answ:=IntToStr(z2);
      end;
    1:begin
        res.question:=res.question+tabl[num mod length(tabl)][0]+'", если известны результаты следующих поисковых запросов:'+chr(10)+
          chr(9)+'* "'+tabl[num mod length(tabl)][0]+'"/"'+tabl[num mod length(tabl)][1]+'" - '+IntToStr(z1)+' тыс. результатов (/ - без)'+chr(10)+
          chr(9)+'* "'+tabl[num mod length(tabl)][0]+'"V"'+tabl[num mod length(tabl)][1]+'" - '+IntToStr(z1+z2+z3)+' тыс. результатов'+chr(10)+
          chr(9)+'* "'+tabl[num mod length(tabl)][0]+'"&"'+tabl[num mod length(tabl)][1]+'" - '+IntToStr(z2)+' тыс. результатов';
          res.answ:=IntToStr(z1+z2);
      end;
    2:begin
        res.question:=res.question+tabl[num mod length(tabl)][1]+'", если известны результаты следующих поисковых запросов:'+chr(10)+
          chr(9)+'* "'+tabl[num mod length(tabl)][0]+'"/"'+tabl[num mod length(tabl)][1]+'" - '+IntToStr(z1)+' тыс. результатов (/ - без)'+chr(10)+
          chr(9)+'* "'+tabl[num mod length(tabl)][0]+'"V"'+tabl[num mod length(tabl)][1]+'" - '+IntToStr(z1+z2+z3)+' тыс. результатов'+chr(10)+
          chr(9)+'* "'+tabl[num mod length(tabl)][0]+'"&"'+tabl[num mod length(tabl)][1]+'" - '+IntToStr(z2)+' тыс. результатов';
          res.answ:=IntToStr(z2+z3);
      end;
  end;
  Qu5:=res;
end;


function qu_6_1(num:integer):que;
var
  res:que;
  x,v,d:integer;
  byt:boolean;
begin
  x:=(num mod 239)+7;
  if(x<101)then x:=x+((x*x) mod 117);
  res.question:='В соревнованиях было '+IntToStr(x)+' участников, никакие два из которых не пришли одновременно.';
  res.question:=res.question+' Сколько нужно времени, чтобы передать информацию о результатах соревнования всех участников, ';
  res.question:=res.question+'если скорость передачи данных равна ';
  case num mod 2 of
    0: byt:=true;
    else byt:=false;
  end;
  d:=length(from10(x,2));
  if(byt) then
    if(d mod 8<>0)then d:=(d div 8)+1
    else d:=d div 8;
  d:=d*x;
  if(byt) then d:=d*8;
  v:=1;
  while ((d mod (2*v))=0)and(2*v <= d) do v:=v*2;
  if(v>=1024)then res.question:=res.question+IntToStr(v div 1024)+'Кб/с?'
  else
    if(v>8)then res.question:=res.question+IntToStr(v div 8)+'Б/с?'
    else res.question:=res.question+IntToStr(v)+'б/с?';
  if(byt) then res.question:=res.question+' Номер каждого участника кодируется целым числом байт.'
  else res.question:=res.question+' Номер каждого участника кодируется целым числом бит.';
  res.answ:=IntToStr(d div v);
  qu_6_1:=res;
end;
function qu_6_2(num:integer):que;
var
  res:que;
  x,y,p,d:integer;
  kol,find:integer;
begin
  x:=(num mod 239)+17;
  x:=((x*x) mod 277)+13;
  x:=((x*x) mod 281)+23;
  if(x<101)then x:=x+((x*x) mod 101);
  res.question:='В соревнованиях было '+IntToStr(x)+' участников, никакие два из которых не пришли одновременно.';
  p:=(num mod 3)+3;
  res.question:=res.question+' Каким наименьшим объемом данных можно закодировать '+IntToStr(p)+'-ку победителей (в битах)?';
  d:=length(from10(x,2));
  d:=d*p;
  res.answ:=IntToStr(d);
  qu_6_2:=res;
end;
function qu_6_3(num:integer):que;
var
  res:que;
  x,v:integer;
begin
  v:=(num mod 11)+7;
  v:=trunc(Power(2,v));
  v:=((num mod 7)+1)*v;
  x:=(((num mod 101)+5)*((num mod 47)+13));
  x:=(x mod 23)+7;
  x:=x*v;
  res.question:='Сколько нужно времени, чтобы передать файл, размером ';
  case x of
    0..1023:
      if(num mod 2=0) and (x mod 8=0) then res.question:=res.question+IntToStr(x div 8)+'Б'
      else res.question:=res.question+IntToStr(x)+'б';
    1024..8191:
      if(num mod 2=0) and (x mod 8=0) then res.question:=res.question+IntToStr(x div 8)+'Б'
      else
      begin
        if(x mod 1024=0)then res.question:=res.question+IntToStr(x div 1024)+'Кб'
        else res.question:=res.question+IntToStr(x div 8)+'Б';
      end;
    else
        if(x mod 1024=0)then
        begin
          if(x mod 8192=0)then res.question:=res.question+IntToStr(x div 8192)+'КБ'
          else res.question:=res.question+IntToStr(x div 1024)+'Кб';
        end
        else res.question:=res.question+IntToStr(x div 8)+'Б';
   end;
  res.question:=res.question+', если скорость передачи данных равна ';
  case v of
    0..7:res.question:=res.question+IntToStr(v)+'б/с?';
    8..1023:
        if(num mod 2=1)and(v mod 8=0)then res.question:=res.question+IntToStr(v div 8)+'Б/с?'
        else res.question:=res.question+IntToStr(v)+'б/с?';
    1024..8191:
        case num mod 11 of
          0..7: res.question:=res.question+IntToStr(v div 8)+'Б/с?';
          else res.question:=res.question+IntToStr(v)+'б/с?';
        end;
    else
      res.question:=res.question+IntToStr(v div 1024)+'Кб/с?';
  end;
  res.answ:=IntToStr(x div v);
  qu_6_3:=res;
end;
function Qu6(num:integer):que;
begin
  num:=num*5;
  case num mod 7 of
    0..2: Qu6:=qu_6_1(num);
    3..5: Qu6:=qu_6_2(num);
    else Qu6:=qu_6_3(num);
  end;
end;

function Qu7(num:integer):PicTask;
var
  res:PicTask;
  nums,i,j,tp,tiers:integer;
  points:array of Point;
  means:array of integer;
  dx:integer;
  places:array of array [0..2] of integer;
  connected:array of array [0..2] of boolean;
  x,y:integer;
  lines:integer;
  x1,x2,y1,y2:integer;
  a:real;
begin
  dx:=80;
  nums:=(num mod 7)+11;
  setLength(points,nums);
  setLength(means,nums);
  means[0]:=1;
  res.task.question:='Сколькими способами можно пройти из вершины "A" в вершину "'+chr(ord('A')+nums-1)+'"';
  if ((nums-2)mod 3<>0)then
    tiers:=((nums-2) div 3)+3
  else
    tiers:=((nums-2) div 3)+2;
  setLength(places,tiers);
  setLength(connected,tiers);
  places[0][0]:=-1; places[0][1]:=0;places[0][2]:=-1;
  places[tiers-1][0]:=-1; places[tiers-1][1]:=nums-1;places[tiers-1][2]:=-1;

  res.pic:=new Picture(tiers*dx,150);
  points[0].X:=15;  points[0].Y:=90;
  points[nums-1].X:=(dx div 2)+(tiers-1)*dx;  points[nums-1].Y:=90;

  i:=1;
  tp:=1;
  while((nums-1)>i)do
  begin
    if((nums-1-i)>=3)then
    begin
      points[i].X:=random(dx div 4,(3*dx) div 4)+dx*tp;
      points[i].Y:=random(7,23);
      places[tp][0]:=i;
      i:=i+1;
      points[i].X:=random(dx div 4,(3*dx) div 4)+dx*tp;
      points[i].Y:=random(7,23)+50;
      places[tp][1]:=i;
      i:=i+1;
      points[i].X:=random(dx div 4,(3*dx) div 4)+dx*tp;
      points[i].Y:=random(7,23)+90;
      places[tp][2]:=i;
      i:=i+1;
      tp:=tp+1;
    end
    else
      if((nums-1-i)=2)then
      begin
        points[i].X:=random(dx div 4,(3*dx) div 4)+dx*tp;
        points[i].Y:=random(7,23);
        places[tp][0]:=i;
        i:=i+1;
        points[i].X:=random(dx div 4,(3*dx) div 4)+dx*tp;
        points[i].Y:=random(7,23)+90;
        places[tp][2]:=i;
        i:=i+1;
        places[tp][1]:=-1;
        tp:=tp+1;
      end
      else
      begin
        points[i].X:=random(dx div 4,(3*dx) div 4)+dx*(tiers-2);
        points[i].Y:=random(-7,23)+50;
        i:=i+1;
        places[tiers-2][0]:=-1;
        places[tiers-2][1]:=i-1;
        places[tiers-2][2]:=-1;
      end;
  end;
  setPenColor(rgb(0,0,0));
  for i:=0 to nums-1 do
  begin
    setBrushColor(rgb(0,0,0));
    res.pic.Circle(points[i].X,points[i].Y,5);
    setBrushColor(rgb(255,255,255));
    res.pic.TextOut(points[i].X-5,points[i].Y+6,chr(ord('A')+i));
  end;
  setBrushColor(rgb(255,255,255));
  
  connected[0][1]:=true; 
  for i:=0 to tiers-2 do
  begin
//    res.pic.Line(dx*(i+1),5,dx*(i+1),120);
    for j:=0 to 2 do
    begin
      if(places[i][j]<>-1)then
      begin
        if(not connected[i][j])then
        begin
          lines:=0;
          if(j>0)then
            if(places[i][j-1]<>-1)then
            begin
              lines:=lines+1;
              means[places[i][j]]:=means[places[i][j-1]];
              connected[i][j]:=true;
              x1:=points[places[i][j-1]].X;   y1:=points[places[i][j-1]].Y;
              x2:=points[places[i][j]].X;     y2:=points[places[i][j]].Y;
              res.pic.Line(x1,y1,x2,y2);
              x:=x1-x2; y:=y1-y2;
              a:=PI - ArcCos((x2-x1)/sqrt(x*x+y*y));
              x:=(x1+7*x2)div 8; y:=(y1+7*y2)div 8;
              res.pic.Line(x+trunc(10*cos(a+PI/10)),y-trunc(10*sin(a+PI/10)),x,y);
              res.pic.Line(x+trunc(10*cos(a-PI/10)),y-trunc(10*sin(a-PI/10)),x,y);
            end;
        end;
        lines:=0;
        if(j>0)then
        begin
          if(places[i+1][j-1]<>-1)then
          begin
            lines:=lines+1;
            means[places[i+1][j-1]]:=means[places[i+1][j-1]]+means[places[i][j]];
            connected[i+1][j-1]:=true;
              x1:=points[places[i][j]].X;     y1:=points[places[i][j]].Y;
              x2:=points[places[i+1][j-1]].X; y2:=points[places[i+1][j-1]].Y;
              res.pic.Line(x1,y1,x2,y2);
              x:=x1-x2; y:=y1-y2;
              a:=PI - ArcSin((y2-y1)/sqrt(x*x+y*y));
              x:=(x1+7*x2)div 8; y:=(y1+7*y2)div 8;
              res.pic.Line(x+trunc(10*cos(a+PI/10)),y-trunc(10*sin(a+PI/10)),x,y);
              res.pic.Line(x+trunc(10*cos(a-PI/10)),y-trunc(10*sin(a-PI/10)),x,y);
          end;
        end;
        if(places[i+1][j]<>-1)then
        begin
          if(lines=0)or(i mod 2=0)then
          begin
            lines:=lines+1;
            means[places[i+1][j]]:=means[places[i+1][j]]+means[places[i][j]];
            connected[i+1][j]:=true;
              x1:=points[places[i][j]].X;     y1:=points[places[i][j]].Y;
              x2:=points[places[i+1][j]].X; y2:=points[places[i+1][j]].Y;
              res.pic.Line(x1,y1,x2,y2);
              x:=x1-x2; y:=y1-y2;
              a:=PI - ArcSin((y2-y1)/sqrt(x*x+y*y));
              x:=(x1+7*x2)div 8; y:=(y1+7*y2)div 8;
              res.pic.Line(x+trunc(10*cos(a+PI/10)),y-trunc(10*sin(a+PI/10)),x,y);
              res.pic.Line(x+trunc(10*cos(a-PI/10)),y-trunc(10*sin(a-PI/10)),x,y);
          end
        end;
        if(j<2)then
        begin
          if(places[i+1][j+1]<>-1)and((lines=0)or(i mod 2=0))then
          begin
            lines:=lines+1;
            means[places[i+1][j+1]]:=means[places[i+1][j+1]]+means[places[i][j]];
            connected[i+1][j+1]:=true;
              x1:=points[places[i][j]].X;     y1:=points[places[i][j]].Y;
              x2:=points[places[i+1][j+1]].X; y2:=points[places[i+1][j+1]].Y;
              res.pic.Line(x1,y1,x2,y2);
              x:=x1-x2; y:=y1-y2;
              a:=PI - ArcSin((y2-y1)/sqrt(x*x+y*y));
              x:=(x1+7*x2)div 8; y:=(y1+7*y2)div 8;
              res.pic.Line(x+trunc(10*cos(a+PI/10)),y-trunc(10*sin(a+PI/10)),x,y);
              res.pic.Line(x+trunc(10*cos(a-PI/10)),y-trunc(10*sin(a-PI/10)),x,y);
          end
        end;
      end;
    end;
  end;
//  res.pic.Save(IntToStr(num)+'.jpg');
//  res.pic.Draw(0,0);
//  Execute(IntToStr(num)+'.jpg');
  res.task.answ:=IntToStr(means[nums-1]);
  Qu7:=res;
end;


var
  task:que;
  taskP:PicTask;
  numVar:integer;
  resultText:text;
  firstNum,step,i:integer;
  date,room,ch:string;
  c:char;
begin
//  c:=readKey;
//  writeln(ord(c));
//  for i:=1 to 10 do
//    taskP:=Qu7(i);
//  writeln(taskP.task);
//  task:=Qu3(10);
//  writeln(task);
  ch:='1';
  while(ch<>'0')do
  begin
    writeln('Наши действия:');
    writeln('1-Создать контрольную');
    writeln('2-Проверить номер');
    writeln('3-Создать домашнюю работу');
    writeln('4-Создать домашнюю работу');
    writeln('0-выход');
    readln(ch);
    if(ch='2')then
    begin
      clrscr();
      firstNum:=1;
      while(firstNum<>0)do
      begin
        writeln('Введите номер варианта или 0, чтобы закончить');
        readln(firstNum);
        task:=Qu1(firstNum);
        writeln('1. ',task.answ);
        task:=Qu2(firstNum);
        writeln('2. ',task.answ);
        task:=Qu3(firstNum);
        writeln('3. ',task.answ);
        task:=Qu4(firstNum);
        writeln('4. ',task.answ);
        task:=Qu5(firstNum);
        writeln('5. ',task.answ);
        task:=Qu6(firstNum);
        writeln('6. ',task.answ);
        taskP:=Qu7(firstNum);
        writeln('7. ',taskP.task.answ);
      end;
    end;
    if(ch='1')then
    begin
      clrscr();
      write('Введите номер первого варианта');
      readln(firstNum);
      writeln(' №',firstNum);
      write('Сколько вариантов сделать');
      readln(numVar);
      writeln(' -',numVar);
      step:=1;
      write('Введите дату контрольной');
      readln(date);
      writeln(' ',date);
      write('Введите класс, для которого будет контрольная');
      readln(room);
      writeln(' - ',room,' класс');
      assign(resultText,'Контрольная.doc');
      resultText.Rewrite();
      for i:=1 to numVar do
      begin
        resultText.Writeln(date,chr(9),room+' класс',chr(9),'Вариант №'+IntToStr(firstNum));
        resultText.Writeln('ФИО:______________________________________________________');
        task:=Qu1(firstNum);
        resultText.Writeln('1. ',task.question);
        resultText.Writeln('Ответ:____________________________________________________');
        task:=Qu2(firstNum);
        resultText.Writeln('2. ',task.question);
        resultText.Writeln('Ответ:____________________________________________________');
        task:=Qu3(firstNum);
        resultText.Writeln('3.',task.question);
        resultText.Writeln('Ответ:____________________________________________________');
        task:=Qu4(firstNum);
        resultText.Writeln('4.',task.question);
        resultText.Writeln('Ответ:____________________________________________________');
        task:=Qu5(firstNum);
        resultText.Writeln('5.',task.question);
        resultText.Writeln('Ответ:____________________________________________________');
        task:=Qu6(firstNum);
        resultText.Writeln('6.',task.question);
        resultText.Writeln('Ответ:____________________________________________________');
        taskP:=Qu7(firstNum);
        resultText.Writeln('7.',taskP.task.question);
        taskP.pic.Save(IntToStr(firstNum)+'.png');
        resultText.Writeln();
        resultText.Writeln('Ответ:____________________________________________________');
        firstNum:=firstNum+step;
        if(i<>numVar)then
          resultText.Writeln(chr(10));
      end;
      resultText.Close();
      Sleep(1000);
      Execute('Контрольная.doc');
      clrscr();
    end;
    if(ch='3')then
    begin
      clrscr();
      write('Введите номер');
      readln(firstNum);
      writeln(' №',firstNum);
      numVar:=1;
      write('Введите дату домашней');
      readln(date);
      writeln(' ',date);
      assign(resultText,'Домашняя работа['+date+'].doc');
      resultText.Rewrite();
        resultText.Writeln('Домашняя работа, ',date,chr(9),' код №'+IntToStr(firstNum));
        resultText.Writeln();
        if(firstNum mod 7>=3)then
          task:=Qu1(firstNum)
        else
          task:=Qu2(firstNum);
        resultText.Writeln('1. ',task.question);
        task:=Qu3(firstNum);
        resultText.Writeln('2.',task.question);
        i:=((firstNum mod 11) div 4);
        resultText.Write('3.');
        task:=Qu4(firstNum+i+1);
        resultText.Writeln(task.question);
        for i:=i downto 0 do
        begin
          if((firstNum+i) mod 2=0)then resultText.Writeln(qu_4_1_ex(firstNum+i).question)
          else resultText.Writeln(qu_4_2_ex(firstNum+i).question);
        end;
        task:=Qu5(firstNum);
        resultText.Writeln('4.',task.question);
        task:=Qu6(firstNum);
        resultText.Writeln('5.',task.question);
        taskP:=Qu7(firstNum);
        resultText.Writeln('6.',taskP.task.question);
        taskP.pic.Save(IntToStr(firstNum)+'.png');
        resultText.Writeln();
        firstNum:=firstNum+step;
      resultText.Close();
      Sleep(1000);
      Execute('Домашняя работа['+date+'].doc');
      clrscr();
    end;
    if(ch='4')then
    begin
      clrscr();
      firstNum:=1;
      while(firstNum<>0)do
      begin
        clrscr();
        write('Введите номер или 0, чтобы закончить');
        readln(firstNum);
        if(firstNum mod 7>=3)then
          task:=Qu1(firstNum)
        else
          task:=Qu2(firstNum);
        writeln('1. ',task.answ);
        task:=Qu3(firstNum);
        Writeln('2.',task.answ);
        i:=((firstNum mod 11) div 4);
        Write('3.');
        task:=Qu4(firstNum+i+1);
        Writeln(task.answ);
        for i:=i downto 0 do
        begin
          if((firstNum+i) mod 2=0)then Writeln(qu_4_1_ex(firstNum+i).answ)
          else Writeln(qu_4_2_ex(firstNum+i).answ);
        end;
        task:=Qu5(firstNum);
        Writeln('4.',task.answ);
        task:=Qu6(firstNum);
        Writeln('5.',task.answ);
        taskP:=Qu7(firstNum);
        Writeln('6.',taskP.task.answ);
        clrscr();
      end;
    end;
  end;
  Window.Close();
end.