## 学生信息数据库 SQL 查询实验

### 1. 实验环境

- **数据库**：`student_inf_20231837`
- **表结构**：
  - `student(Sno, Sname, Sex, Birthdate, EnrollDate, Sdept, Postcode)`
  - `course(Cno, Cname, Credit, TotalHours)`
  - `sc(Sno, Cno, Grade)`
- **工具**：Navicat for MySQL（截图中的客户端）

> 以下所有 SQL 语句均在 `student_inf_20231837` 库中执行，语法基于 MySQL 8.0。

### 0. 数据准备脚本（可选）

为便于复现实验，可先执行以下脚本初始化表数据。若已有同名记录，可在执行前 `TRUNCATE` 对应表，或把 `INSERT` 改为 `REPLACE/ON DUPLICATE KEY UPDATE`。

```sql
-- 0.1 创建数据库与三张表（如已存在可跳过）
CREATE DATABASE IF NOT EXISTS student_inf_20231837 CHARACTER SET utf8mb4;
USE student_inf_20231837;

CREATE TABLE IF NOT EXISTS student (
    Sno       CHAR(8) PRIMARY KEY,
    Sname     VARCHAR(20),
    Sex       ENUM('男','女'),
    Birthdate DATE,
    EnrollDate DATE,
    Sdept     VARCHAR(10),
    Postcode  VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS course (
    Cno        CHAR(3) PRIMARY KEY,
    Cname      VARCHAR(40),
    Credit     DECIMAL(3,1),
    TotalHours INT
);

CREATE TABLE IF NOT EXISTS sc (
    Sno   CHAR(8),
    Cno   CHAR(3),
    Grade DECIMAL(5,2),
    PRIMARY KEY (Sno, Cno),
    FOREIGN KEY (Sno) REFERENCES student(Sno),
    FOREIGN KEY (Cno) REFERENCES course(Cno)
);

-- 0.2 学生样例数据
INSERT INTO student (Sno, Sname, Sex, Birthdate, EnrollDate, Sdept, Postcode) VALUES
('20231837', '陈星宇', '男', '2004-05-20', '2023-09-01', '2023371', '200001'),
('20250001', '张三',   '男', '2004-03-01', '2022-09-01', '2023371', '200001'),
('20250002', '李四',   '女', '2004-07-15', '2022-09-01', '2023371', '200001'),
('20250003', '王五',   '男', '2003-10-10', '2022-09-01', '2023372', '200002'),
('20250004', '张虹',   '女', '2004-01-05', '2022-09-01', '2023372', '200003'),
('20250005', '李虹',   '女', '2003-12-20', '2022-09-01', '2023371', '200004'),
('20250006', '林峰',   '男', '2004-06-18', '2022-09-01', '2023372', '200005'),
('20250007', '赵敏',   '女', '2003-09-25', '2022-09-01', '2023373', '200006'),
('20250008', '刘备',   '男', '2004-02-14', '2022-09-01', '2023373', '200007'),
('20250009', '张伟',   '男', '2003-11-30', '2022-09-01', '2023371', '200008'),
('20250010', '林红',   '女', '2004-04-08', '2022-09-01', '051',      '200009'),
('20251011', '周杰',   '男', '2003-08-12', '2022-09-01', '051',      '200010'),
('20251012', '李敏',   '女', '2004-09-22', '2022-09-01', '051',      '200011'),
('20251013', '王倩',   '女', '2004-02-02', '2022-09-01', '051',      '200012');

-- 0.3 课程样例数据
INSERT INTO course (Cno, Cname, Credit, TotalHours) VALUES
('001', '高等数学',     5.0, 80),
('002', '数据结构',     4.0, 64),
('003', 'C语言程序设计', 3.0, 48),
('004', 'Visual_Basic', 3.0, 48),
('005', '数据库原理',   4.0, 64),
('006', '操作系统',     3.5, 56);

-- 0.4 选课成绩数据
INSERT INTO sc (Sno, Cno, Grade) VALUES
('20231837', '001', 86.5),
('20231837', '002', 90.0),
('20231837', '003', 78.0),
('20250001', '001', 85.0),
('20250001', '002', 92.0),
('20250001', '003', 88.0),
('20250001', '005', 81.0),
('20250002', '001', 76.0),
('20250002', '003', 79.0),
('20250002', '005', NULL),
('20250003', '002', 88.0),
('20250003', '003', 92.0),
('20250003', '004', 75.0),
('20250004', '001', 83.0),
('20250004', '002', 80.0),
('20250004', '006', 89.0),
('20250005', '003', 68.0),
('20250005', '004', 72.0),
('20250005', '005', 90.0),
('20250006', '001', 91.0),
('20250006', '005', 87.0),
('20250006', '006', 84.0),
('20250007', '002', 70.0),
('20250007', '003', 66.0),
('20250007', '005', 73.0),
('20250008', '003', 88.0),
('20250008', '004', 82.0),
('20250008', '006', 79.0),
('20250009', '001', 69.0),
('20250009', '002', 74.0),
('20250009', '003', 60.0),
('20250010', '001', 77.0),
('20250010', '002', 81.0),
('20250010', '003', 86.0),
('20250010', '006', 88.0),
('20251011', '001', 82.0),
('20251011', '003', 84.0),
('20251011', '005', 79.0),
('20251012', '001', 93.0),
('20251012', '002', 88.0),
('20251012', '006', 91.0),
('20251013', '002', 76.0),
('20251013', '003', 83.0),
('20251013', '005', 85.0);
```

> 上述数据覆盖题目中出现的全部姓名、课程与成绩（包括“林红”），执行完即可确保每条查询都有对应样本。

### 2. 查询题目与 SQL 实现

#### （1）查询比“林红”年纪大的男学生信息
```sql
SELECT *
FROM student
WHERE Sex = '男'
  AND Birthdate < (
      SELECT Birthdate
      FROM student
      WHERE Sname = '林红'
  );
```
**说明**：若查询结果为空，通常是因为表中不存在姓名为“林红”的记录或其出生日期为 `NULL`。可改用实际存在的姓名（如“张虹”）或先确认/插入对应数据。

#### （2）查询所有学生的选课信息（含未选课）
```sql
SELECT s.Sno, s.Sname, sc.Cno, c.Cname, sc.Grade
FROM student AS s
LEFT JOIN sc ON sc.Sno = s.Sno
LEFT JOIN course AS c ON c.Cno = sc.Cno
ORDER BY s.Sno, sc.Cno;
```

#### （3）查询已选课学生的学号、姓名、课程名、成绩
```sql
SELECT DISTINCT s.Sno, s.Sname, c.Cname, sc.Grade
FROM student AS s
JOIN sc ON sc.Sno = s.Sno
JOIN course AS c ON c.Cno = sc.Cno
ORDER BY s.Sno, c.Cno;
```

#### （4）查询选修“C语言程序设计”的学生学号和姓名
```sql
SELECT DISTINCT s.Sno, s.Sname
FROM student AS s
JOIN sc ON sc.Sno = s.Sno
JOIN course AS c ON c.Cno = sc.Cno
WHERE c.Cname = 'C语言程序设计';
```

#### （5）查询与“张虹”同班学生的学号、姓名、家庭住址
```sql
SELECT s.Sno, s.Sname, s.Postcode AS HomeAddress
FROM student AS s
WHERE s.Sdept = (
        SELECT Sdept
        FROM student
        WHERE Sname = '张虹'
    )
ORDER BY s.Sno;
```

#### （6）查询其他班级中比“051”班所有学生年龄大的学生
```sql
SELECT s.Sno, s.Sname, s.Sdept, s.Birthdate
FROM student AS s
WHERE s.Sdept <> '051'
  AND s.Birthdate < (
      SELECT MIN(Birthdate)
      FROM student
      WHERE Sdept = '051'
  );
```

#### （7）查询选修全部课程的学生姓名
```sql
SELECT s.Sname
FROM student AS s
JOIN sc AS sc1 ON sc1.Sno = s.Sno
GROUP BY s.Sno, s.Sname
HAVING COUNT(DISTINCT sc1.Cno) = (SELECT COUNT(*) FROM course);
```

#### （8）查询至少选修了“20110002”所选全部课程的学生
```sql
SELECT s.Sno, s.Sname
FROM student AS s
WHERE NOT EXISTS (
          SELECT 1
          FROM sc AS t
          WHERE t.Sno = '20110002'
            AND NOT EXISTS (
                    SELECT 1
                    FROM sc AS mine
                    WHERE mine.Sno = s.Sno
                      AND mine.Cno = t.Cno
                )
      );
```

#### （9）查询学生的学号、姓名、课程名及成绩
```sql
SELECT s.Sno, s.Sname, c.Cname, sc.Grade
FROM sc
JOIN student AS s ON s.Sno = sc.Sno
JOIN course  AS c ON c.Cno = sc.Cno
ORDER BY s.Sno, c.Cno;
```

#### （10）查询满足条件的高数成绩并降序排列
```sql
SELECT sc.Sno, sc.Cno, sc.Grade
FROM sc
JOIN course AS c ON c.Cno = sc.Cno
WHERE c.Cname = '高等数学'
  AND sc.Grade >= (
        SELECT Grade
        FROM sc
        WHERE Sno = sc.Sno
          AND Cno = '002'
    )
ORDER BY sc.Grade DESC;
```

#### （11）查询选修 3 门以上课程学生的合格总成绩
```sql
SELECT s.Sno,
       s.Sname,
       COUNT(DISTINCT sc.Cno) AS CourseCount,
       SUM(CASE WHEN sc.Grade >= 60 THEN sc.Grade ELSE 0 END) AS PassedTotal
FROM student AS s
JOIN sc ON sc.Sno = s.Sno
GROUP BY s.Sno, s.Sname
HAVING COUNT(DISTINCT sc.Cno) > 3
ORDER BY PassedTotal DESC;
```

#### （12）查询多于 3 名学生选修且课号以 3 结尾的课程平均成绩
```sql
SELECT c.Cno,
       c.Cname,
       AVG(sc.Grade) AS AvgGrade,
       COUNT(DISTINCT sc.Sno) AS StudentCount
FROM course AS c
JOIN sc ON sc.Cno = c.Cno
WHERE c.Cno LIKE '%3'
GROUP BY c.Cno, c.Cname
HAVING COUNT(DISTINCT sc.Sno) > 3;
```

#### （13）查询最高分与最低分之差大于 5 分的学生
```sql
SELECT s.Sno,
       s.Sname,
       MAX(sc.Grade) AS MaxGrade,
       MIN(sc.Grade) AS MinGrade,
       MAX(sc.Grade) - MIN(sc.Grade) AS Diff
FROM student AS s
JOIN sc ON sc.Sno = s.Sno
GROUP BY s.Sno, s.Sname
HAVING MAX(sc.Grade) - MIN(sc.Grade) > 5;
```

#### （14）查询每名同学分数最高的两门课
```sql
WITH ranked AS (
    SELECT sc.Sno,
           sc.Cno,
           c.Cname,
           sc.Grade,
           ROW_NUMBER() OVER (
               PARTITION BY sc.Sno
               ORDER BY sc.Grade DESC
           ) AS rn
    FROM sc
    JOIN course AS c ON c.Cno = sc.Cno
)
SELECT r.Sno, s.Sname, r.Cno, r.Cname, r.Grade
FROM ranked AS r
JOIN student AS s ON s.Sno = r.Sno
WHERE r.rn <= 2
ORDER BY r.Sno, r.Grade DESC;
```

#### （15）`student_other` 表及集合操作
```sql
CREATE TABLE IF NOT EXISTS student_other LIKE student;

INSERT INTO student_other (...)
VALUES (...); -- 插入若干与 student 表部分重复的记录

-- a. 交集
SELECT s.*
FROM student AS s
JOIN student_other AS o ON o.Sno = s.Sno;

-- b. 并集
SELECT * FROM student
UNION
SELECT * FROM student_other;
```

### 3. 多数据库间的多表查询

```sql
CREATE DATABASE IF NOT EXISTS student_info_other DEFAULT CHARACTER SET utf8mb4;

CREATE TABLE student_info_other.student_other LIKE student_inf_20231837.student_other;

INSERT INTO student_info_other.student_other
SELECT * FROM student_inf_20231837.student_other;

SELECT s.*
FROM student_inf_20231837.student AS s
JOIN student_info_other.student_other AS o ON o.Sno = s.Sno;
```

### 4. 外连接与补充查询

#### （1）课程及其选课信息（含未选修）
```sql
SELECT c.Cno, c.Cname, sc.Sno, sc.Grade
FROM course AS c
LEFT JOIN sc ON sc.Cno = c.Cno
ORDER BY c.Cno, sc.Sno;
```

#### （2）学生与课程的完全外连接效果
```sql
SELECT s.Sno, s.Sname, c.Cno, c.Cname, sc.Grade
FROM student AS s
LEFT JOIN sc ON sc.Sno = s.Sno
LEFT JOIN course AS c ON c.Cno = sc.Cno
UNION
SELECT s.Sno, s.Sname, c.Cno, c.Cname, sc.Grade
FROM course AS c
LEFT JOIN sc ON sc.Cno = c.Cno
LEFT JOIN student AS s ON s.Sno = sc.Sno;
```

#### （补充）无不及格且班级加权平均成绩前 10
```sql
WITH weighted AS (
    SELECT s.Sdept,
           s.Sno,
           s.Sname,
           SUM(sc.Grade * c.Credit) / SUM(c.Credit) AS WeightedAvg,
           ROW_NUMBER() OVER (
               PARTITION BY s.Sdept
               ORDER BY SUM(sc.Grade * c.Credit) / SUM(c.Credit) DESC
           ) AS rn
    FROM student AS s
    JOIN sc ON sc.Sno = s.Sno
    JOIN course AS c ON c.Cno = sc.Cno
    WHERE sc.Grade IS NOT NULL
      AND NOT EXISTS (
            SELECT 1
            FROM sc AS fail
            WHERE fail.Sno = s.Sno
              AND fail.Grade < 60
        )
    GROUP BY s.Sdept, s.Sno, s.Sname
)
SELECT Sdept, Sno, Sname, WeightedAvg
FROM weighted
WHERE rn <= 10
ORDER BY Sdept, WeightedAvg DESC;
```

### 5. 实验小结

1. **查询策略**：综合使用子查询、聚合、窗口函数、集合操作与连接，覆盖常见 SQL 题型。
2. **数据依赖**：部分查询（如“林红”）依赖特定记录，如无匹配需先新增样本或替换为现有姓名。
3. **扩展方向**：可将这些 SQL 封装为视图或存储过程，结合截图与执行结果撰写实验报告。

> 建议在执行前用 `SELECT * FROM student WHERE Sname = '林红';` 检查数据是否存在，必要时先 `INSERT` 测试记录，避免空结果导致的困惑。

