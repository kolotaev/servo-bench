package controllers

import javax.inject._
import play.api._
import play.api.mvc._
import play.api.libs.json._
import models._


@Singleton
class HomeController @Inject()(cc: ControllerComponents) extends AbstractController(cc) {

  def index() = Action { implicit request: Request[AnyContent] =>
     Ok(views.html.index())
  }

  def json() = Action { implicit request: Request[AnyContent] =>
    val p: Person = Person(true)
    Ok(Json.toJson(p))
  }

  def db() = Action { implicit request: Request[AnyContent] =>
    Ok(views.html.index())
  }
}
