"""
 Loads Box2D world from json file generated by R.U.B.E. to pyBox2D world
"""
import Box2D as b2
import json


def createWorldFromJson(filePathName):
    """
    # loads json from file to memory
    # and returns b2_world from it
    """
    # load json into memory
    with open(filePathName, "r") as json_file:
        jsw = json.load(json_file)

    # create world from json data
    b2_world = create_world(jsw)

    # fill world with bodies and joints
    add_bodies(b2_world, jsw)
    add_joints(b2_world, jsw)

    return b2_world


def add_joints(
        b2_world,
        jsw,  # json world
        ):
    if "joint" in jsw.keys():
        # add joints to world
        for joint in jsw["joint"]:
            add_joint(b2_world, jsw, joint)


def add_bodies(
        b2_world,
        jsw,  # json world
        ):
    if "body" in jsw.keys():
        # add bodies to world
        for js_body in jsw["body"]:
            add_body(b2_world, jsw, js_body)


def create_world(
        jsw,  # json world
        ):
    return b2.b2World(
        autoClearForces=jsw["autoClearForces"],
        continuousPhysics=jsw["continuousPhysics"],
        gravity=rubeVecToB2Vec2(jsw["gravity"]),
        subStepping=jsw["subStepping"],
        warmStarting=jsw["warmStarting"],
        )


def add_joint(
        b2_world,
        jsw,  # json world
        jsw_joint
        ):
    # create definition
    jointDef = create_jointDef(jsw_joint, b2_world)

    # create joint from definition
    b2_world.CreateJoint(jointDef, jsw_joint["type"])


# NOTE: no custom properties impplemented
# refer to rube, box2d and pybox2d documentation
def create_jointDef(jsw_joint, b2_world):
    joint_type = jsw_joint["type"]  # naming

    #---------------------------------------------------
    if joint_type == "revolute":  # Done
        jointDef = b2.b2RevoluteJointDef()

        jointDef.bodyA = get_body(b2_world, jsw_joint["bodyA"])
        jointDef.bodyB = get_body(b2_world, jsw_joint["bodyB"])
        setB2Vec2Attr(jsw_joint, "anchorA", jointDef, "localAnchorA")
        setB2Vec2Attr(jsw_joint, "anchorB", jointDef, "localAnchorB")
        setAttr(jsw_joint, "collideConnected", jointDef)
        setAttr(jsw_joint, "enableLimit", jointDef)
        setAttr(jsw_joint, "enableMotor", jointDef)
        setAttr(jsw_joint, "jointSpeed", jointDef, "motorSpeed")
        setAttr(jsw_joint, "lowerLimit", jointDef, "lowerAngle")
        setAttr(jsw_joint, "maxMotorTorque", jointDef)
        setAttr(jsw_joint, "motorSpeed", jointDef)
        setAttr(jsw_joint, "refAngle", jointDef, "referenceAngle")
        setAttr(jsw_joint, "upperLimit", jointDef, "upperAngle")

    #---------------------------------------------------
    elif joint_type == "distance":  # Done
        jointDef = b2.b2DistanceJointDef()

        jointDef.bodyA = get_body(b2_world, jsw_joint["bodyA"])
        jointDef.bodyB = get_body(b2_world, jsw_joint["bodyB"])
        setB2Vec2Attr(jsw_joint, "anchorA", jointDef, "localAnchorA")
        setB2Vec2Attr(jsw_joint, "anchorB", jointDef, "localAnchorB")
        setAttr(jsw_joint, "collideConnected", jointDef)
        setAttr(jsw_joint, "dampingRatio", jointDef)
        setAttr(jsw_joint, "frequency", jointDef, "frequencyHz")
        setAttr(jsw_joint, "length", jointDef)

    #---------------------------------------------------
    elif joint_type == "prismatic":  # Done
        jointDef = b2.b2PrismaticJointDef()

        jointDef.bodyA = get_body(b2_world, jsw_joint["bodyA"])
        jointDef.bodyB = get_body(b2_world, jsw_joint["bodyB"])
        setB2Vec2Attr(jsw_joint, "anchorA", jointDef, "localAnchorA")
        setB2Vec2Attr(jsw_joint, "anchorB", jointDef, "localAnchorB")
        setAttr(jsw_joint, "collideConnected", jointDef)
        setAttr(jsw_joint, "enableLimit", jointDef)
        setAttr(jsw_joint, "enableMotor", jointDef)
        setB2Vec2Attr(jsw_joint, "localAxisA", jointDef, "localAxis1")
        setAttr(jsw_joint, "lowerLimit", jointDef, "lowerTranslation")
        setAttr(jsw_joint, "maxMotorForce", jointDef)
        setAttr(jsw_joint, "motorSpeed", jointDef)
        setAttr(jsw_joint, "refAngle", jointDef, "referenceAngle")
        setAttr(jsw_joint, "upperLimit", jointDef, "upperTranslation")

    #---------------------------------------------------
    elif joint_type == "wheel":  # Done
        jointDef = b2.b2WheelJointDef()

        jointDef.bodyA = get_body(b2_world, jsw_joint["bodyA"])
        jointDef.bodyB = get_body(b2_world, jsw_joint["bodyB"])
        setB2Vec2Attr(jsw_joint, "anchorA", jointDef, "localAnchorA")
        setB2Vec2Attr(jsw_joint, "anchorB", jointDef, "localAnchorB")
        setAttr(jsw_joint, "collideConnected", jointDef)
        setAttr(jsw_joint, "enableMotor", jointDef)
        setB2Vec2Attr(jsw_joint, "localAxisA", jointDef)
        setAttr(jsw_joint, "maxMotorTorque", jointDef)
        setAttr(jsw_joint, "motorSpeed", jointDef)
        setAttr(jsw_joint, "springDampingRatio", jointDef, "dampingRatio")
        setAttr(jsw_joint, "springFrequency", jointDef, "frequencyHz")

    #---------------------------------------------------
    elif joint_type == "rope":  # Done
        jointDef = b2.b2RopeJointDef()

        jointDef.bodyA = get_body(b2_world, jsw_joint["bodyA"])
        jointDef.bodyB = get_body(b2_world, jsw_joint["bodyB"])
        setB2Vec2Attr(jsw_joint, "anchorA", jointDef, "localAnchorA")
        setB2Vec2Attr(jsw_joint, "anchorB", jointDef, "localAnchorB")
        setAttr(jsw_joint, "collideConnected", jointDef)
        setAttr(jsw_joint, "maxLength", jointDef)

    #---------------------------------------------------
    elif joint_type == "motor":  # Doesn't properly work
        # missing linearOffset
        jointDef = b2.b2MotorJointDef()

        jointDef.bodyA = get_body(b2_world, jsw_joint["bodyA"])
        jointDef.bodyB = get_body(b2_world, jsw_joint["bodyB"])
        setB2Vec2Attr(jsw_joint, "anchorA", jointDef, "localAnchorA")
        setB2Vec2Attr(jsw_joint, "anchorB", jointDef, "localAnchorB")
        setAttr(jsw_joint, "collideConnected", jointDef)
        setAttr(jsw_joint, "maxForce", jointDef)
        setAttr(jsw_joint, "maxTorque", jointDef)
        setAttr(jsw_joint, "angularOffset", jointDef)
        setAttr(jsw_joint, "correctionFactor", jointDef)

    #---------------------------------------------------
    elif joint_type == "weld":  # Done
        jointDef = b2.b2WeldJointDef()

        jointDef.bodyA = get_body(b2_world, jsw_joint["bodyA"])
        jointDef.bodyB = get_body(b2_world, jsw_joint["bodyB"])
        setB2Vec2Attr(jsw_joint, "anchorA", jointDef, "localAnchorA")
        setB2Vec2Attr(jsw_joint, "anchorB", jointDef, "localAnchorB")
        setAttr(jsw_joint, "collideConnected", jointDef)
        setAttr(jsw_joint, "refAngle", jointDef, "referenceAngle")
        setAttr(jsw_joint, "dampingRatio", jointDef)
        setAttr(jsw_joint, "frequency", jointDef, "frequencyHz")

    #---------------------------------------------------
    elif joint_type == "friction":  # Done
        jointDef = b2.b2FrictionJointDef()

        jointDef.bodyA = get_body(b2_world, jsw_joint["bodyA"])
        jointDef.bodyB = get_body(b2_world, jsw_joint["bodyB"])
        setB2Vec2Attr(jsw_joint, "anchorA", jointDef, "localAnchorA")
        setB2Vec2Attr(jsw_joint, "anchorB", jointDef, "localAnchorB")
        setAttr(jsw_joint, "collideConnected", jointDef)
        setAttr(jsw_joint, "maxForce", jointDef)
        setAttr(jsw_joint, "maxTorque", jointDef)

    else:
        print ("unsupported joint type")

    return jointDef


def get_body(b2_world, index):
    return b2_world.bodies[index]


def add_body(
        b2_world,  #
        jsw,  # loaded json b2World
        jsw_body
        ):
        # create body definition
        bodyDef = b2.b2BodyDef()

        # Done with minor issues
        # missing pybox2d inertiaScale
        setAttr(jsw, "allowSleep", bodyDef)
        setAttr(jsw_body, "angle", bodyDef)
        setAttr(jsw_body, "angularDamping", bodyDef)
        setAttr(jsw_body, "angularVelocity", bodyDef)
        setAttr(jsw_body, "awake", bodyDef)
        setAttr(jsw_body, "bullet", bodyDef)
        setAttr(jsw_body, "fixedRotation", bodyDef)
        setAttr(jsw_body, "linearDamping", bodyDef)
        setB2Vec2Attr(jsw_body, "linearVelocity", bodyDef)
        setB2Vec2Attr(jsw_body, "position", bodyDef)
        setAttr(jsw_body, "gravityScale", bodyDef)  # pybox2d non documented
        # setAttr(jsw_body, "massData-I", bodyDef, "inertiaScale")
        setAttr(jsw_body, "type", bodyDef)
        setAttr(jsw_body, "awake", bodyDef)

        # create body
        body_ref = b2_world.CreateBody(bodyDef)

        for fixture in jsw_body["fixture"]:
            add_fixture(body_ref, jsw, fixture)


# TODO: solve open chains.
# Can't. Don't understand pyBox2D documentation
def add_fixture(
        b2_world_body,
        jsw,
        jsw_fixture,
        ):
     # create and fill fixture definition
    fixtureDef = b2.b2FixtureDef()

    # Done with issues
    # missing pybox2d "filter" b2BodyDef property
    setAttr(jsw_fixture, "density", fixtureDef)
    setAttr(jsw_fixture, "filter-categoryBits", fixtureDef, "categoryBits")
    setAttr(jsw_fixture, "filter-maskBits", fixtureDef, "maskBits")
    setAttr(jsw_fixture, "filter-groupIndex", fixtureDef, "groupIndex")
    setAttr(jsw_fixture, "friction", fixtureDef)
    setAttr(jsw_fixture, "sensor", fixtureDef, "isSensor")
    setAttr(jsw_fixture, "restitution", fixtureDef)

    # fixture has one shape that is
    # polygon, circle or chain in json
    # chain may be open or loop, or edge in pyBox2D
    if "circle" in jsw_fixture.keys():  # works ok
        if jsw_fixture["circle"]["center"] == 0:
            center_b2Vec2 = b2.b2Vec2(0, 0)
        else:
            center_b2Vec2 = rubeVecToB2Vec2(
                jsw_fixture["circle"]["center"]
                )
        fixtureDef.shape = b2.b2CircleShape(
            pos=center_b2Vec2,
            radius=jsw_fixture["circle"]["radius"],
            )

    if "polygon" in jsw_fixture.keys():  # works ok
        polygon_vertices = rubeVecArrToB2Vec2Arr(
            jsw_fixture["polygon"]["vertices"]
            )
        fixtureDef.shape = b2.b2PolygonShape(vertices=polygon_vertices)

    if "chain" in jsw_fixture.keys():  # doesn't properly work
        chain_vertices = rubeVecArrToB2Vec2Arr(
            jsw_fixture["chain"]["vertices"]
            )

        # BUGS!: open ended creates +1 vertice chain
        # loop shape crashes
        # edge works ok

        # json chain is b2ChainShape
        if len(chain_vertices) >= 3:
            # closed-loop ChainShape
            # BUG: crashes
            if "hasNextVertex" in jsw_fixture.keys():
                #setAttr(jsw_fixture, "hasNextVertex", fixtureDef)
                #setB2Vec2Attr(jsw_fixture, "nextVertex", fixtureDef)
                #setAttr(jsw_fixture, "hasPrevVertex", fixtureDef)
                #setB2Vec2Attr(jsw_fixture, "prevVertex", fixtureDef)

                fixtureDef.shape = b2.b2ChainShape(
                    vertices=chain_vertices,
                    count=len(chain_vertices),
                    )
            else:  # open-ended ChainShape
                # BUG: creates closed chainShape with +1 vertice
                fixtureDef.shape = b2.b2ChainShape(
                    vertices=chain_vertices,
                    count=len(chain_vertices),
                    )

                # trying to follow original Box2D manual
                # following fails
                #fixtureDef.shape = b2.b2ChainShape()
                #fixtureDef.shape.CreateChain(
                #    vertices=chain_vertices,
                #    count=len(chain_vertices),
                #    )

        # json chain is b2EdgeShape
        if len(chain_vertices) < 3:
            fixtureDef.shape = b2.b2EdgeShape(
                vertices=chain_vertices,
                )

    # create fixture
    b2_world_body.CreateFixture(fixtureDef)


def setAttr(
        source_dict,
        source_key,  # dict_source's key
        target_obj,  # obj with attribute 'key' or 'renamed'
        target_attr=None,  # target attribute == key if is None
        ):
    """
    # assigns values from dict to target object, if key exists in dict
    # may take renamed attribute for object
    # works only with built_in values
    """
    if source_key in source_dict.keys():
        if not target_attr:
            target_attr = source_key
        if hasattr(target_obj, target_attr):
            setattr(target_obj, target_attr, source_dict[source_key])
        else:
            print("No attr: " + target_attr + " in object")
    # debug helper
    #else:
    #    print "No key '" + source_key + "' in dict '" + source_dict["name"] + "'"


def rubeVecToB2Vec2(rube_vec):
    # converter from rube json vector to b2Vec2
    return b2.b2Vec2(rube_vec["x"], rube_vec["y"])


def rubeVecArrToB2Vec2Arr(vector_array):
    """
    # converter from rube json vector array to b2Vec2 array
    """
    return [b2.b2Vec2(x, y) for x, y in zip(
            vector_array["x"],
            vector_array["y"]
            )]


def setB2Vec2Attr(
        source_dict,
        source_key,
        target_obj,
        target_attr=None,  # is source_key if None
        ):
    if source_key in source_dict.keys():
        # setting attr name
        if target_attr is None:
            target_attr = source_key

        # preparing B2Vec
        if source_dict[source_key] == 0:
            vec2 = b2.b2Vec2(0, 0)
        else:
            vec2 = rubeVecToB2Vec2(source_dict[source_key])

        # setting obj's attr value
        setattr(target_obj, target_attr, vec2)
    #else:
    #    print "No key '" + key + "' in dict '" + dict_source["name"] + "'"


if __name__ == "__main__":  # fast test
    filePathName = "d:\\jointTypes.json"
    b2_world = None

    b2_world = createWorldFromJson(filePathName)
    #print b2_world.autoClearForces
    #print b2_world.__repr__()