var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../server.js');
var should = chai.should();

chai.use(chaiHttp);

describe('User', function() {

  it('should save a user to mongo locally (try testing spotiy auth later)', function(done) {
    chai.request(server)
    .get('/')
    .end(function(err, res){
      res.should.have.status(200);
      done();
    })
  });

  // it('should save a user to mongo on soundcloud auth callback');
  it('should show user profile on /GET profile');

  // it('should add a SINGLE blob on /blobs POST');
  // it('should update a SINGLE blob on /blob/<id> PUT');
  // it('should delete a SINGLE blob on /blob/<id> DELETE');
});