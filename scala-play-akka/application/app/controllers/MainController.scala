package controllers

import javax.inject._
import scala.concurrent.ExecutionContext.Implicits.global

import play.api._
import play.api.mvc._
import play.api.libs.json._

import models._
import repositories._


@Singleton
class MainController @Inject()(cc: ControllerComponents, repository: PersonRepository)
  extends AbstractController(cc) {

  def index() = Action { implicit request =>
     Ok(views.html.index())
  }

  def json() = Action { implicit request =>
    val p: Person = Person(true)
    Ok(Json.toJson(p))
  }

  def db() = Action.async { implicit request =>
    repository.getAll(2) map {
      case _ => Ok(Json.toJson(Map("AL" -> "Alabama", "AK" -> "Alaska")))
//      case None => NotFound
    }
  }
}
