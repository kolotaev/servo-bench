package controllers

import javax.inject._
import scala.concurrent.ExecutionContext.Implicits.global
import scala.util.{Random, Properties}

import play.api._
import play.api.mvc._
import play.api.libs.json._

import models.{Person, Result}
import repositories.{PersonRepository}


@Singleton
class MainController @Inject()(cc: ControllerComponents, repository: PersonRepository)
  extends AbstractController(cc) {

  val sqlMaxSleep = Properties.envOrElse("SQL_SLEEP_MAX", "0.0").toFloat // seconds
  val loopCount = Properties.envOrElse("LOOP_COUNT", "0").toInt

  def index() = Action { implicit request =>
     Ok(views.html.index())
  }

  def json() = Action { implicit request =>
    val p: Person = Person(true)
    Ok(Json.toJson(p))
  }

  def db() = Action.async { implicit request =>
    val qry = if (sqlMaxSleep == 0) {
      "SELECT count(*) FROM pg_catalog.pg_user"
    } else {
      val sleep = Random.nextDouble * sqlMaxSleep
      s"SELECT pg_sleep($sleep)"
    }
    repository.doQuery(qry) map {
      case _ => {
        // Create some CPU and RAM load
        val persons = for (_ <- 0 until loopCount) yield Person(true)

        Ok(Json.toJson(new Result(qry, loopCount, persons)))
      }
    }
  }
}
