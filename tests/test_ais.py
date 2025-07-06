from src.ais import replay_ais


def test_replay_ais(capsys, tmp_path):
    log = tmp_path / "ais.log"
    content = (
        "!AIVDM,1,1,,A,15MuqA?P00PD;088K4<`w?vP0200,0*58\n"
        "!AIVDM,1,1,,A,15MuqA?P00PD;088K4<`w?vP0200,0*58\n"
    )
    log.write_text(content)
    replay_ais(str(log))
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == [
        "!AIVDM,1,1,,A,15MuqA?P00PD;088K4<`w?vP0200,0*58",
        "!AIVDM,1,1,,A,15MuqA?P00PD;088K4<`w?vP0200,0*58",
    ]
