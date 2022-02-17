create table TNoticiero(
idNoticiero int primary key identity(1,1),
id varchar(30),
name varchar(30)
)

create table TArticulo(
idArticulo int primary key identity(1,1),
idNoticiero int foreign key references TNoticiero(idNoticiero),
author nvarchar(100),
title nvarchar(250),
description nvarchar(261),
url varchar(2048),
urlToImage varchar(2048),
publishedAt char(20),
content nvarchar(275),
)