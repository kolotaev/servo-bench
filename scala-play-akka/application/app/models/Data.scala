package models

import scala.util.Random._
import play.api.libs.json._


case class Person(name: String, surname: String, street: String, school: String,
                  bank: String, a: Int, b: Double, c: Int, friends: List[Person])

object Person {
  implicit val personWrites = new Writes[Person] {
    def writes(p: Person) = Json.obj(
      "name" -> p.name,
      "surname" -> p.surname,
      "street" -> p.street,
      "school" -> p.school,
      "bank" -> p.bank,
      "a" -> p.a,
      "b" -> p.b,
      "c" -> p.c,
      "friends" -> JsArray(p.friends.map(x => Json.toJson(x)(this)))
    )
  }

  def apply(hasFriend: Boolean = false): Person = {
    new Person(
      name = alphanumeric.take(10).mkString,
      surname = alphanumeric.take(3).mkString,
      street = alphanumeric.take(15).mkString,
      school = alphanumeric.take(9).mkString,
      bank = alphanumeric.take(4).mkString,
      a = nextInt(100),
      b = nextDouble,
      c = nextInt(1090),
      friends = if (hasFriend) List(Person()) else List()
    )
  }
}

case class Result(query: String, loop: Long, data: Seq[Person])

object Result {
  implicit val personWrites = new Writes[Result] {
    def writes(r: Result) = Json.obj(
      "query" -> r.query,
      "loop-count" -> r.loop,
      "data"  -> r.data
    )
  }
}
