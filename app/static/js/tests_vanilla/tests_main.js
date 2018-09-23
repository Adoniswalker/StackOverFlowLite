describe('This will test share functions in main.js', () => {
    it("Should test trimming of variables", ()=>{
        expect(trimfield(" dennis ")).toBe("dennis");
    })
});
describe('Will test prettydate humanisation', ()=>{
    let now = "2018-09-21 02:00:00.890626";
    it("Should test a just now", ()=>{
        expect(prettyDate("2018-09-21 01:59:30.890626", now)).toBe("just now");
    });
    it("Should test a minute ago", ()=>{
        expect(prettyDate("2018-09-21 01:58:30.890626", now)).toBe("1 minute ago");
    });
    it("Should test 5 minutes ago", ()=>{
        expect(prettyDate("2018-09-21 01:54:30.890626", now)).toBe("5 minutes ago");
    });
    it("Should test a hour ago", ()=>{
        expect(prettyDate("2018-09-21 00:59:30.890626", now)).toBe("an hour ago");
    });
    it("Should test 5 hours ago ago", ()=>{
        expect(prettyDate("2018-09-20 20:00:30.890626", now)).toBe("5 hours ago");
    });
    it("Should test yesterday", ()=>{
        expect(prettyDate("2018-09-20 01:59:30.890626", now)).toBe("Yesterday");
    });
    it("Should test last week", ()=>{
        expect(prettyDate("2018-09-13 02:00:00.890626", now)).toBe("last week");
    });
    it("Should test 3 weeks ago", ()=>{
        expect(prettyDate("2018-09-02 01:59:30.890626", now)).toBe("3 weeks ago");
    });
    it("Should test last month", ()=>{
        expect(prettyDate("2018-08-21 01:59:30.890626", now)).toBe("last month");
    });
    it("Should test 5 months ago", ()=>{
        expect(prettyDate("2018-05-21 01:59:30.890626", now)).toBe("5 months ago");
    });
    it("Should test last year", ()=>{
        expect(prettyDate("2017-05-21 01:59:30.890626", now)).toBe("last year");
    })
    ;
    it("Should test 5 years ago", ()=>{
        expect(prettyDate("2014-09-21 01:59:30.890626", now)).toBe("5 years ago");
    });
    it("Should test future dates", ()=>{
        expect(prettyDate("2019-09-21 01:59:30.890626", now)).toBe(undefined);
    })
});
describe("This will test the cookie",()=>{
    xit("Test creation of cookie", ()=>{
        expect(createCookie("token","hdsjjndsnkldskmdsmklsdllsd;ldsldl", 4)).toBe("token=hdsjjndsnkldskmdsmklsdllsd;ldsldl; expires=Tue, 25 Sep 2018 08:30:44 GMT");
    })
});
describe("Working with sinon", ()=>{
    function once(fn) {
        var returnValue, called = false;
        return function () {
            if (!called) {
                called = true;
                returnValue = fn.apply(this, arguments);
            }
            return returnValue;
        };
    }
    it('calls the original function', function () {
        var callback = sinon.fake.returns(42);
        var proxy = once(callback);

        expect(proxy()).toEqual(42);

    });
});