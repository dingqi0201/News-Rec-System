# Created by Fufu at 2019/10/9
@bgp
Feature: BGP管理
  请先清除数据(暂未开放删除操作)
  delete from ff_bgp where bgp_asn in (1, 99999990);

  @success
  Scenario Outline: 1. 添加 BGP (正例)
    Given 输入BGP-IP, ASN和描述 "<bgp_ip>", "<bgp_asn>", "<bgp_desc>", "<bgp_test_float>"
    When 执行添加BGP操作
    Then BGP-IP添加成功

    Examples:
      | bgp_ip      | bgp_asn  | bgp_desc     | bgp_test_float |
      | 127.0.0.127 | 1        | test_bgp     | 1.2356         |
      | 17.0.0.17   | 1        | test_bgp_ok  | 6              |
      | 8.8.8.1     | 99999990 | test_bgp_??? | 0              |

  @error
  Scenario Outline: 2. 添加 BGP (反例)
    Given 输入BGP-IP和描述, ASN错误 "<bgp_ip>", "<bgp_asn>", "<bgp_desc>", "<bgp_test_float>"
    When 执行添加BGP操作
    Then BGP添加失败

    Examples:
      | bgp_ip   | bgp_asn  | bgp_desc | bgp_test_float |
      | 1.1.1.1  | 99999998 | test_1   | 0              |
      | 1.1.1.1  | 0        | test_1   | 0.0            |
      | 10.0.0.1 | a123     | 123      | 0.00           |
      | 0.0.0.1  | -1       | test     | 1.23           |

  @error
  Scenario Outline: 3. 添加 BGP (反例)
    Given BGP-IP输入错误 "<bgp_ip>", "<bgp_asn>", "<bgp_desc>", "<bgp_test_float>"
    When 执行添加BGP操作
    Then BGP添加失败

    Examples:
      | bgp_ip       | bgp_asn  | bgp_desc     | bgp_test_float |
      | abc          | 1        | test_bgp     | 1              |
      | -1           | 1        | test_bgp     | 1              |
      | 127.0.0.256  | 1        | test_bgp     | 1              |
      | 127.0.0.1127 | 1        | test_bgp     | 1              |
      | 8.8.8.       | 99999990 | test_bgp_??? | 1              |
      | 123          | 1        | test_bgp     | 1              |

  @error
  Scenario Outline: 2. 添加 BGP (反例)
    Given 浮点数输入错误 "<bgp_ip>", "<bgp_asn>", "<bgp_desc>", "<bgp_test_float>"
    When 执行添加BGP操作
    Then BGP添加失败

    Examples:
      | bgp_ip  | bgp_asn | bgp_desc   | bgp_test_float |
      | 7.0.0.7 | 1       | test_bgp_1 | a              |
      | 7.0.0.7 | 1       | test_bgp_1 | -1             |
