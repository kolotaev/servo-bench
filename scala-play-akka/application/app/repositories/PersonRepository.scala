package repositories

import java.sql.Connection
import java.util.concurrent.Executors
import javax.inject.{Inject, Singleton}
import scala.concurrent.{ExecutionContext, Future}

import anorm.SqlParser._
import anorm._
import play.api.db.Database

import models._


@Singleton
class PersonRepository @Inject()(db: Database) {

  implicit val ec: ExecutionContext = ExecutionContext.fromExecutor(
    Executors.newFixedThreadPool(Properties.envOrElse("POOL_SIZE", "1").toInt)
  )

  val personParser = float("pg_sleep") map {
    case _ => true
  }

  def withDb[T](body: Connection => T): Future[T] = Future(db.withConnection(body(_)))

  def doQuery(query: String) = withDb { implicit conn =>
    val result: Boolean = SQL(query).execute()
  }
}
