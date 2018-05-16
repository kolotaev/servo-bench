package controllers

import javax.inject._
import play.api._
import play.api.mvc._
import play.api.libs.json._

import models._
import repositories._


@Singleton
class HomeController @Inject()(cc: ControllerComponents) extends AbstractController(cc) {

  def index() = Action { implicit request =>
     Ok(views.html.index())
  }

  def json() = Action { implicit request =>
    val p: Person = Person(true)
    Ok(Json.toJson(p))
  }

  def db() = Action.async { implicit request =>
    repository.getTodo(id) map {
      case Some(todo) => Ok(Json.toJson(TodoView.fromModel(todo)))
      case None => NotFound
    }
  }
}
