from arg import parser 
import log
import conf
import server



if __name__ == "__main__":
   args = parser.parse_args()
   _config = conf.start(
     args,
     log.logging,
   )
   log.start(
     _config
   )
   server.start(
     log.logging,
     _config
  )
