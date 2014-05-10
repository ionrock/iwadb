=====================
 I Wrote a Database!
=====================

Long ago and far away I used a simple database built on bsddb. It was
fast, simple and designed for our specific application. The problem
was that we wanted replication. We wanted to make multiple copies of
our data.

IWADB (I Wrote a DataBase) is meant to be similar to that store with
the biggest difference being you get replication. There isn't a crazy
query language or anything. No specialized indexes. Just a dumb REST
interface.

What is that? Why even use it?

Whoa pard'ner! You're not supposed to actually use IWADB! It is
something I did for fun that I doubt has much practical value. Maybe
someday, but that day isn't today.


Under the Hood
==============

The only reason I can imagine IWADB could ever turn out to be
something valuable is that it uses some powerful systems.

Rather than use bsddb, we're using lmdb. It is a great key value store
that has a nifty feature of ordering its keys. Lmdb is really fast and
well tested.

For replication, we're using Kafka. Kafka is a really slick durable
queue. You can configure it to keep as much stuff as you want and it
is able to scale out to many instances without much trouble. IWADB was
written to have an excuse to play with Kafka.

Last but not least, we're using CherryPy! CherryPy has the benefit of
being a good citizen when it comes to processes and it has excellent
support for HTTP.
