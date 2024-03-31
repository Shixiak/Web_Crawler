-- 注释

-- 创建表格
-- not null  非空约束. 该列数据不可以为空
-- primary key  这一列是主键. 全表唯一. 不能重复
-- auto_increment  自动增长. 不用我们维护
create table stu(
	sno int(5) not null  primary key auto_increment,
	sname varchar(50) not null, 
	sage int(3)
)

-- 删除表格
drop table stu;


-- 添加数据  insert into xxx(字段, 字段,) values (值1, 值2,)
insert into stu(sname, sage, school) values ("李嘉诚", 18, "沙河小学");
insert into stu(sname, sage, school) values ("渣渣辉", 28, "巩华家园小学");
insert into stu(sname, sage, school) values ("张翠山", 38, "师大附小");

-- 删除数据  delete from xxxx where 条件
delete from stu where sno = 4 ;
delete from stu;

-- 修改数据 update xxx set 字段 = 值, 字段2 = 值2.... where 条件
update stu set sage = 79 where sno = 5;
update stu set sage = 79, school = '鹤北镇小学' where sno = 5;

-- 查询
-- 简单查询 select *|字段1, 字段2, 字段3... from xxx
select * from stu;
select sname as `姓名`, school as `学校` from stu;

-- 带条件的查询语句  where
select * from stu where sage = 28;
select * from stu where sage > 28;

-- 不等于: <>  !=
select * from stu where sage <> 28;
select * from stu where sage != 28;

-- 年龄在28-56之间的人的信息
select * from stu where sage between 28 and 56;

-- 查询姓李的人的信息
select * from stu where sname like '李%';

-- 查询年龄是28, 38的人
select * from stu where sage in (28, 38);

-- 通过and和or进行连接
select * from stu where sage = 28 or sage = 38;
-- select * from stu where username  = ? and password = ?



-- 创建一个学生表
create table stu_new(
	sno int(5) primary key auto_increment,
	sname varchar(30),
	sgender int(2),
	sage int(5),
	score int(5),
	class varchar(50)
)

insert into stu_new(sname, sgender, sage, score, class) values 
("赵本山", 1, 65, 90, "一年二班"),
("范伟", 1, 60, 23, "一年二班"),
("小沈阳", 1, 31, 9, "一年一班"),
("沈春阳", 2, 28, 60, "一年一班"),
("严启航", 1, 18, 99, "一年一班"),
("赵四", 1, 38, -9, "一年三班"),
("武则天", 2, 1300, 67, "一年三班");


-- 统计每个班级的平均成绩是多少
-- 聚合函数, sum(), count(), avg(), max(), min()
-- 聚合函数一般和group by子句搭配使用
-- group by 分组
-- 规定. 凡事没有放在聚合函数内的东西. 都要堆在group by 后面
select class, avg(score) from stu_new group by class;

-- 统计男生女生有多少人
select sgender, count(*), avg(score),max(score), min(score) from stu_new group by sgender;

-- 统计每个班级的男生女生数量
select class, sgender, count(*) from stu_new group by class, sgender;

-- 对统计结果进行筛选, having 条件
-- 统计出平均成绩合格的班级
select class, avg(score) from stu_new group by class having avg(score) >= 60;


-- 排序
select * from stu_new order by score asc;
select * from stu_new order by score desc;

-- limit 
select * from stu_new limit 3

select * from stu_new limit 3

